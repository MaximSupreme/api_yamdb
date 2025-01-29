from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

import api.serializers as serializers
import reviews.models as models
from api.viewsets import ListCreateDeleteViewset
from user.permissions import IsAdminOrReadOnly


class TitleViewset(viewsets.ModelViewSet):
    queryset = models.Title.objects.all()
    serializer_class = serializers.TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')
    permission_classes = [IsAdminOrReadOnly,]


class GenreViewset(ListCreateDeleteViewset):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [IsAdminOrReadOnly,]


class CategoryViewset(ListCreateDeleteViewset):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [IsAdminOrReadOnly,]
