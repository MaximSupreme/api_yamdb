from http import HTTPStatus

import django_filters
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

import api.serializers as serializers
import reviews.models as models
from api.viewsets import ListCreateDeleteViewset
from api.filters import TitleFilter
from api.permissions import (
    IsAdminModeratorAuthorOrReadOnly, IsAdminUserOrReadOnly
)
from api.serializers import (
    AdminUserSerializer,
    CustomUserSerializer,
    TokenSerializer,
    UserRegistrationSerializer
)
from api.permissions import IsAdminOrReadOnly, IsAdmin
from api.filters import CustomUserFilter


CustomUser = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = models.Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('rating')
    serializer_class = serializers.TitleSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def perform_create(self, serializer):
        category = get_object_or_404(
            models.Category, slug=self.request.data.get('category')
        )
        genre = models.Genre.objects.filter(
            slug__in=self.request.data.getlist('genre')
        )
        serializer.save(category=category, genre=genre)

    def perform_update(self, serializer):
        self.perform_create(serializer)


class GenreViewSet(ListCreateDeleteViewset):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)

    def destroy(self, request, *args, **kwargs):
        slug = kwargs.get('pk')
        instance = get_object_or_404(models.Genre, slug=slug)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(ListCreateDeleteViewset):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)

    def destroy(self, request, *args, **kwargs):
        slug = kwargs.get('pk')
        instance = get_object_or_404(models.Category, slug=slug)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminModeratorAuthorOrReadOnly
    )

    def get_queryset(self):
        title = get_object_or_404(
            models.Title, id=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            models.Title, id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminModeratorAuthorOrReadOnly
    )

    def get_queryset(self):
        review = get_object_or_404(
            models.Review, id=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            models.Review, id=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter
    )
    search_fields = ('username',)
    filterset_class = CustomUserFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self):
        if self.action in ('signup', 'token'):
            return []
        if self.action == 'me':
            return [IsAuthenticated()]
        return [IsAdmin()]

    def get_serializer_class(self):
        if self.action == 'signup':
            return UserRegistrationSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return AdminUserSerializer
        return CustomUserSerializer

    def get_object(self):
        if self.action == 'me':
            return self.request.user
        username = self.kwargs.get('username')
        return get_object_or_404(CustomUser, username=username)

    @action(
        detail=False,
        methods=['get', 'patch', 'delete'],
        permission_classes=[IsAuthenticated],
        url_path='me'
    )
    def me(self, request):
        if request.method == 'DELETE':
            return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=HTTPStatus.OK)

    @action(detail=False, methods=['post'])
    def token(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                'token': str(serializer.validated_data['token'])
            },
            status=HTTPStatus.OK
        )