from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.permissions import IsAdmin
from user.serializers import (
    AdminUserSerializer,
    CustomUserSerializer,
    TokenSerializer,
    UserRegistrationSerializer
)
from user.utils import (
    confirmation_code_generator, customed_send_mail
)


CustomUser = get_user_model()


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
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

    def get_queryset(self):
        queryset = CustomUser.objects.all().order_by('username')
        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(username__icontains=search)
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=HTTPStatus.NO_CONTENT)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=HTTPStatus.CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        try:
            user = CustomUser.objects.get(email=email)
            if user.username == username:
                confirmation_code = confirmation_code_generator()
                user.confirmation_code = confirmation_code
                user.save()
                customed_send_mail(email, confirmation_code)
                return Response(serializer.data, status=HTTPStatus.OK)
            else:
                return Response(
                    {
                        'detail': (
                            'User with that email is already exists. '
                            'Check your entered username.'
                        )
                    },
                    status=HTTPStatus.BAD_REQUEST
                )
        except CustomUser.DoesNotExist:
            try:
                user = CustomUser.objects.get(username=username)
                if user.email == email:
                    confirmation_code = confirmation_code_generator()
                    user.confirmation_code = confirmation_code
                    user.save()
                    customed_send_mail(email, confirmation_code)
                    return Response(serializer.data, status=HTTPStatus.OK)
                else:
                    return Response(
                        {
                            'detail':
                            'User with that username is already exists. '
                            'Check your entered email.'
                        },
                        status=HTTPStatus.BAD_REQUEST
                    )
            except CustomUser.DoesNotExist:
                user = CustomUser.objects.create(
                    username=username, email=email
                )
                confirmation_code = confirmation_code_generator()
                user.confirmation_code = confirmation_code
                user.save()
                customed_send_mail(email, confirmation_code)
                return Response(serializer.data, status=HTTPStatus.OK)

    @action(detail=False, methods=['post'])
    def token(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response(
                {'detail': 'Пользователь не найден'},
                status=HTTPStatus.NOT_FOUND
            )
        if user.confirmation_code != confirmation_code:
            return Response(
                {'token': 'Неверный код подтверждения'},
                status=HTTPStatus.BAD_REQUEST
            )
        token = confirmation_code_generator()
        return Response({'token': str(token)}, status=HTTPStatus.OK)
