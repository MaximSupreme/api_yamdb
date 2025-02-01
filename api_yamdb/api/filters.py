from django_filters.rest_framework import CharFilter, FilterSet

from reviews.models import Title
from user.models import CustomUser


class TitleFilter(FilterSet):
    category = CharFilter(field_name='category__slug')
    name = CharFilter(lookup_expr='icontains')
    genre = CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ['year']


class CustomUserFilter(FilterSet):
    username = CharFilter(
        field_name='username', lookup_expr='icontains'
    )

    class Meta:
        model = CustomUser
        fields = ['username']
