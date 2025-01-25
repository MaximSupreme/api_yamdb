from rest_framework import serializers
from django.shortcuts import get_object_or_404

import reviews.models as models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = models.Title
        fields = '__all__'

    def create(self, validated_data):
        category, status = models.Category.objects.get_or_create(
            **validated_data.pop('category')
        )
        title = models.Title.objects.create(
            **validated_data,
            category=category
        )

        genres = validated_data.pop('genres')
        for genre in genres:
            current_genre, status = models.Genre.objects.get_or_create(**genre)
            models.TitleGenre.objects.create(
                title=title, genre=current_genre
            )


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.StringRelatedField()
    author = serializers.StringRelatedField()
    score = serializers.IntegerField()
    pub_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = models.Review
        fields = ('title', 'author', 'score', 'pub_date', 'text')

    def validate(self, value):
        request = self.context['request']
        author = request.user
        title_id = request.parser_context['kwargs'].get('title_id')

        title = get_object_or_404(models.Title, id=title_id)

        if request.method == 'POST' and title.reviews.filter(
                author=author).exists():
            raise serializers.ValidationError(
                f'Отзыв на "{title.name}" был добавлен ранее'
            )

        return value

    def validate_score(self, value):
        if not (1 <= value <= 10):
            raise serializers.ValidationError(
                "Оценка должна быть между 1 и 10.")
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ('author', 'review', 'text', 'pub_date')
        model = models.Comment
