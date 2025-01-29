from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .permissions import IsAdminModeratorAuthorOrReadOnly
import api.serializers as serializers
import reviews.models as models
from api.viewsets import ListCreateDeleteViewset


class TitleViewSet(viewsets.ModelViewSet):
    queryset = models.Title.objects.all().order_by('name')
    serializer_class = serializers.TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')


class GenreViewSet(ListCreateDeleteViewset):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(ListCreateDeleteViewset):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminModeratorAuthorOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(models.Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(models.Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = (
    permissions.IsAuthenticatedOrReadOnly, IsAdminModeratorAuthorOrReadOnly)

    def get_queryset(self):
        review = get_object_or_404(models.Review,
                                   id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(models.Review,
                                   id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    @action(detail=True, methods=['put'], url_path='update',
            permission_classes=[permissions.IsAdminUser])
    def not_allowed_update(self, request, *args, **kwargs):
        return Response(
            {'detail': 'PUT method is not allowed on this resource.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED)
