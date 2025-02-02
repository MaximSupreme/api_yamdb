from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import serializers, exceptions, validators

from reviews.models import Category, Comment, Genre, Review, Title
from api.constants import (
    MAX_LENGTH_FIRST_LAST_AND_USERNAME,
    MAX_STRING_CHAR, ROLE_USER, ROLES
)
from user.utils import (
    username_validator,
    confirmation_code_generator,
    customed_send_mail
)


CustomUser = get_user_model()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Genre


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True,)
    rating = serializers.FloatField(read_only=True)
    category = CategorySerializer()

    class Meta:
        fields = '__all__'
        read_only_fields = ('category', 'rating', 'genre')
        model = Title


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug',
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    score = serializers.IntegerField(
        validators=[
            MinValueValidator(
                1, message='The score must be at least 1!'),
            MaxValueValidator(
                10, message='The score should not be higher than 10!')
        ]
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, value):
        author = self.context['request'].user
        title_id = (self.context['request'].
                    parser_context['kwargs'].get('title_id'))
        title = get_object_or_404(
            Title,
            id=title_id
        )
        if (self.context['request'].method == 'POST'
                and title.reviews.filter(author=author).exists()):
            raise serializers.ValidationError(
                f'A review of {title.name} is already exists!'
            )
        return value

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


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
            raise serializers.ValidationError(
                'Username "me" is not allowed'
            )
        return value

    def validate(self, attrs):
        username = attrs['username']
        email = attrs['email']
        users = CustomUser.objects.filter(
            Q(username=username) | Q(email=email)
        )
        if not users:
            user = CustomUser.objects.create(username=username, email=email)
            confirmation_code = confirmation_code_generator()
            user.confirmation_code = confirmation_code
            user.save()
            customed_send_mail(email, confirmation_code)
            return attrs
        user = next(
            (
                user
                for user in users
                if user.username == username and user.email == email
            ),
            None
        )
        if user:
            confirmation_code = confirmation_code_generator()
            user.confirmation_code = confirmation_code
            user.save()
            customed_send_mail(email, confirmation_code)
            return attrs
        for user in users:
            if user.username == username:
                raise serializers.ValidationError(
                    'User with that username is already exists. '
                    'Check your entered email.'
                )
            if user.email == email:
                raise serializers.ValidationError(
                    'User with that email is already exists. '
                    'Check your entered username.'
                    )


class AdminUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=MAX_STRING_CHAR,
        required=True,
        validators=[validators.UniqueValidator(
            queryset=CustomUser.objects.all(),
            message='User with that email is already exists!')]
    )
    username = serializers.CharField(
        max_length=MAX_LENGTH_FIRST_LAST_AND_USERNAME,
        required=True,
        validators=[
            username_validator, validators.UniqueValidator(
                queryset=CustomUser.objects.all(),
                message='User with that username is already exists!'
            )
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
    bio = serializers.CharField(
        max_length=MAX_STRING_CHAR,
        required=False
    )
    role = serializers.ChoiceField(
        choices=ROLES, default=ROLE_USER, required=False
    )

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_FIRST_LAST_AND_USERNAME
    )
    confirmation_code = serializers.CharField()

    def validate_username(self, value):
        return username_validator(value)

    def validate(self, attrs):
        username = attrs['username']
        confirmation_code = attrs['confirmation_code']
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise exceptions.NotFound({'detail': 'User not found!'})
        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError({'token': 'Wrong access code!'})
        token = confirmation_code_generator()
        attrs['token'] = token
        return attrs


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
