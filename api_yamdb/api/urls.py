from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewset, GenreViewset, TitleViewset)
from user.views import CustomUserViewSet

router_v1 = DefaultRouter()
router_v1.register(
    'users',
    CustomUserViewSet,
    basename='users'
)
router_v1.register(
    'titles',
    TitleViewset,
    basename='titles'
)
router_v1.register(
    'categories',
    CategoryViewset,
    basename='categories'
)
router_v1.register(
    'genres',
    GenreViewset,
    basename='genre'
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
