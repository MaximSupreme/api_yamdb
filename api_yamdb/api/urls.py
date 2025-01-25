from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

import api.views as views

router_v1 = DefaultRouter()
router_v1.register(
    'titles',
    viewset=views.TitleViewset,
    basename='titles'
)
router_v1.register(
    'categories',
    viewset=views.CategoryViewset,
    basename='categories'
)
router_v1.register(
    'genres',
    viewset=views.GenreViewset,
    basename='genre'
)

urls = [
    path('', include(router_v1.urls)),
    # тут нужно будет добавить пути для работы с юзерами
]

urlpatterns = [
    path('v1/', include(urls)),
    path('auth/token/', TokenObtainPairView().as_view(), name='token_obtain_pair'),
]
