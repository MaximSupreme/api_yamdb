from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.core.validators import MaxValueValidator, MinValueValidator

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Category

    def validate_slug(self, value):
        if self.instance:
            if (Category.objects.filter(slug=value)
                    .exclude(id=self.instance.id).exists()):
                raise serializers.ValidationError(
                    'Category with that slug is already exists!')
        else:
            if Category.objects.filter(slug=value).exists():
                    raise serializers.ValidationError(
                        'Category with that slug is already exists!')
        return value


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Genre

    def validate_slug(self, value):
        if self.instance:
            if (Genre.objects.filter(slug=value)
                    .exclude(id=self.instance.id).exists()):
                raise serializers.ValidationError(
                    'Genre with that slug is already exists!')
        else:
            if Genre.objects.filter(slug=value).exists():
                raise serializers.ValidationError(
                    'Genre with that slug is already exists!')
        return value

class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)
    category = CategorySerializer(read_only=True)

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
                1, message='The score must be at least 1'),
            MaxValueValidator(
                10, message='The score should not be higher than 10')
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
                f'A review of {title.name} is already exists.'
            )
        return value

    def create(self, validated_data):
        review = super().create(validated_data)
        review.title.update_rating()
        return review

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
