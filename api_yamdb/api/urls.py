from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                    ReviewViewSet, CommentViewSet)
from user.views import CustomUserViewSet


router_v1 = DefaultRouter()
router_v1.register(
    'users',
    CustomUserViewSet,
    basename='users'
)
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genre'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)


urls = [
    path('', include(router_v1.urls)),
]

auth_patterns = [
    path('signup/', CustomUserViewSet.as_view({'post': 'signup'}), name='signup'),
    path('token/', CustomUserViewSet.as_view({'post': 'token'}), name='token'),
]

urlpatterns = [
    path('v1/', include(urls)),
    path('v1/auth/', include(auth_patterns)),
]