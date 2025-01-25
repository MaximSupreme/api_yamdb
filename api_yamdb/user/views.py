from rest_framework import viewsets
from django.contrib.auth import get_user_model

from .serializers import CustomUserSerializer


CustomUser = get_user_model()

class UserViewSet(viewsets.ModelViewSet): 
    queryset = CustomUser.objects.all() 
    serializer_class = UserSerializer 
    pagination_class = PageNumberPagination 
    permission_classes = (IsAdmin,) 
    lookup_field = 'username' 
    filter_backends = (filters.SearchFilter,) 
    search_fields = ('username',) 
    http_method_names = ['get', 'post', 'patch', 'delete'] 
 
    def get_permissions(self): 
        """ 
        Возвращает список разрешений для различных действий. 
        """ 
        if self.action in ('signup', 'token'): 
            return [] 
        if self.action == 'me': 
            return [IsAuthenticated()] 
        return [IsAdmin()] 
 
    def get_serializer_class(self): 
        """Определяет класс сериализатора в зависимости от действия.""" 
        if self.action == 'signup': 
            return SignupSerializer 
        if self.action in ['create', 'update', 'partial_update']: 
            return AdminUserSerializer 
        return UserSerializer 
 
    def get_object(self): 
        """Получает объект пользователя для текущего запроса.""" 
        if self.action == 'me': 
            return self.request.user 
        username = self.kwargs.get('username') 
        return get_object_or_404(User, username=username) 
 
    @action( 
        detail=False, 
        methods=['get', 'patch', 'delete'], 
        permission_classes=[IsAuthenticated], 
        url_path='me' 
    ) 
    def me(self, request): 
        """Позволяет пользователю получить и изменить свои данные.""" 
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
        """Возвращает отфильтрованный QuerySet пользователей.""" 
        queryset = User.objects.all().order_by('username') 
        search = self.request.query_params.get('search', None) 
        if search is not None: 
            queryset = queryset.filter(username__icontains=search) 
        return queryset 
 
    def destroy(self, request, *args, **kwargs): 
        """Удаляет пользователя.""" 
        instance = self.get_object() 
        self.perform_destroy(instance) 
        return Response(status=HTTPStatus.NO_CONTENT) 
 
    def create(self, request, *args, **kwargs): 
        """Создает нового пользователя.""" 
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
        """Сохраняет нового пользователя.""" 
        serializer.save() 
 
    def update(self, request, *args, **kwargs): 
        """Обновляет данные пользователя.""" 
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
        """Сохраняет обновленные данные пользователя.""" 
        serializer.save() 
 
    @action(detail=False, methods=['post']) 
    def signup(self, request): 
        """ 
        Регистрирует нового пользователя. 
 
        или 
 
        обновляет код подтверждения существующего. 
        """ 
        serializer = SignupSerializer(data=request.data) 
        serializer.is_valid(raise_exception=True) 
 
        username = serializer.validated_data['username'] 
        email = serializer.validated_data['email'] 
 
        user, _ = User.objects.get_or_create( 
            username=username, 
            email=email 
        ) 
 
        confirmation_code = generate_confirmation_code() 
        user.confirmation_code = confirmation_code 
        user.save() 
 
        custom_send_mail(email, confirmation_code) 
 
        return Response(serializer.data, status=HTTPStatus.OK) 
 
    @action(detail=False, methods=['post']) 
    def token(self, request): 
        """Создает JWT-токен для пользователя по коду подтверждения.""" 
        serializer = TokenSerializer(data=request.data) 
        serializer.is_valid(raise_exception=True) 
        username = serializer.validated_data['username'] 
        confirmation_code = serializer.validated_data['confirmation_code'] 
        try: 
            user = User.objects.get(username=username) 
        except User.DoesNotExist: 
            return Response( 
                {'detail': 'Пользователь не найден'}, 
                status=HTTPStatus.NOT_FOUND 
            ) 
 
        if user.confirmation_code != confirmation_code: 
            return Response( 
                {'token': 'Неверный код подтверждения'}, 
                status=HTTPStatus.BAD_REQUEST 
            ) 
 
        token = generate_confirmation_code() 
        return Response({'token': str(token)}, status=HTTPStatus.OK)
