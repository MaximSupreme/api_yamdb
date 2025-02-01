from datetime import datetime as dt

from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Avg

from api.constants import MAX_SLUG_CHAR, MAX_STRING_CHAR
from user.models import CustomUser


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        max_length=MAX_STRING_CHAR
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=MAX_SLUG_CHAR,
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        max_length=MAX_STRING_CHAR
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=MAX_SLUG_CHAR,
        unique=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

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
    genre = models.ManyToManyField(
        verbose_name='Жанр',
        to=Genre,
        blank=True,
        related_name='title',
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        verbose_name='Категория',
        to=Category,
        on_delete=models.CASCADE,
        related_name='title',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def update_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            avg_rating = reviews.aggregate(
                Avg('score')
            )['score__avg']
            self.rating = avg_rating
            self.save()

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Текст обзора')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        null=True
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_review'
            )
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Обзор'
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации комментария',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
