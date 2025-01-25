from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from api.constants import MAX_STRING_CHAR, MAX_LENGTH_FIRST_LAST_AND_USERNAME


CustomUser = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('usernam', 'email')
    
    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Username "me" is not allowed')
        return value
    
    def validate(self, data):
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Username already exists')
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Email already exists.')
        return data


class AdminUserSerializer(serializers.ModelSerializer): 
    email = serializers.EmailField( 
        max_length=MAX_STRING_CHAR, 
        required=True, 
        validators=[serializers.UniqueValidator( 
            queryset=CustomUser.objects.all(), 
            message="Пользователь с таким email уже существует")] 
    ) 
    username = serializers.CharField( 
        max_length=MAX_LENGTH_FIRST_LAST_AND_USERNAME, 
        required=True, 
        validators=[validate_username_custom, 
                    serializers.UniqueValidator( 
                        queryset=CustomUser.objects.all(), 
                        message="Пользователь с таким username уже существует") 
                    ] 
    ) 
    first_name = serializers.CharField( 
        max_length=MAX_LENGTH_FIRST_LAST_AND_USERNAME, 
        required=False 
    ) 
    last_name = serializers.CharField( 
        max_length=MAX_LENGTH_FIRST_LAST_AND_USERNAME, 
        required=False 
    )

    class Meta: 
        model = CustomUser 
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role') 


class TokenSerializer(serializers.Serializer): 
    username = serializers.CharField(max_length=MAX_LENGTH_FIRST_LAST_AND_USERNAME) 
    confirmation_code = serializers.CharField()

    def validate_username(self, value): 
        return validate_username_custom(value) 


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField( 
        max_length=MAX_LENGTH_FIRST_LAST_AND_USERNAME, 
        validators=[validate_username_custom] 
    ) 
    email = serializers.EmailField( 
        max_length=MAX_STRING_CHAR
    ) 
    first_name = serializers.CharField( 
        max_length=MAX_LENGTH_FIRST_LAST_AND_USERNAME, 
        required=False 
    ) 
    last_name = serializers.CharField( 
        max_length=MAX_LENGTH_FIRST_LAST_AND_USERNAME, 
        required=False 
    )

    class Meta: 
        model = CustomUser 
        fields = ( 
            'username', 'email', 'first_name', 
            'last_name', 'bio', 'role' 
        ) 
        read_only_fields = ('role',)
