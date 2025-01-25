from datetime import datetime as dt

from django.core.validators import MaxValueValidator
from django.db import models

from reviews.constants import MAX_SLUG_CHAR, MAX_STRING_CHAR


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        max_length=MAX_STRING_CHAR
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=MAX_SLUG_CHAR
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        max_length=MAX_STRING_CHAR
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=MAX_SLUG_CHAR
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Заголовок',
        max_length=MAX_STRING_CHAR
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        validators=[
            MaxValueValidator(
                limit_value=dt.now().year
            )
        ]
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        verbose_name='Жанр',
        to=Genre,
        through='TitleGenre',
        related_name='Произведение',
    )
    category = models.ForeignKey(
        verbose_name='Категория',
        to=Category,
        on_delete=models.CASCADE,
        related_name='Произведение'
    )

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        to=Title,
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        to=Genre,
        on_delete=models.CASCADE
    )
