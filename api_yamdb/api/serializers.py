from rest_framework import serializers

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
