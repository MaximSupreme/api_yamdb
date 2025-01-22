from rest_framework import mixins, viewsets


class ListCreateDeleteViewset(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
):
    pass
