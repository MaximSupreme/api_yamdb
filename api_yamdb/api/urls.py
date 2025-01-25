from django.urls import include, path
from rest_framework.routers import DefaultRouter

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
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)


urls = [
    path('', include(router_v1.urls)),
    # тут нужно будет добавить пути для работы с юзерами
]

'''Такой финт ушами со списом юрл нужен для корректного ведения учета версий
внутри приложения api, а не за его пределами'''

urlpatterns = [
    path('v1/', include(urls)),
]
