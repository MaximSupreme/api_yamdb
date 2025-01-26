from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.constants import MAX_LENGTH_FIRST_LAST_AND_USERNAME, MAX_STRING_CHAR

from .utils import username_validator

CustomUser = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=MAX_STRING_CHAR,
        required=True
    )
    username = serializers.CharField(
        max_length=MAX_LENGTH_FIRST_LAST_AND_USERNAME,
        required=True,
        validators=[username_validator]
    )
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

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
        validators=[UniqueValidator(
            queryset=CustomUser.objects.all(),
            message='User with that email is already exists!')]
    )
    username = serializers.CharField(
        max_length=MAX_LENGTH_FIRST_LAST_AND_USERNAME,
        required=True,
        validators=[username_validator,
                    UniqueValidator(
                        queryset=CustomUser.objects.all(),
                        message='User with that username is already exists!')
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
        return username_validator(value)


class CustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_FIRST_LAST_AND_USERNAME,
        validators=[username_validator]
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
