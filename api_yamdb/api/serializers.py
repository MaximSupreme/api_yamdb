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
    class Meta:
        model = models.Title
        fields = '__all__'
