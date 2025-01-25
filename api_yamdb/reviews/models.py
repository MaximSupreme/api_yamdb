from datetime import datetime as dt

from django.core.validators import MaxValueValidator, MinValueValidator
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


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.IntegerField(null=True, blank=True)
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='reviews',
    # )
    score = models.IntegerField(null=True)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.IntegerField(null=True, blank=True)
    # author = models.ForeignKey(
    #     to=User,
    #     verbose_name="Автор комментария",
    #     on_delete=models.CASCADE,
    #     related_name="comments"
    # )
    title = models.ForeignKey(
        to=Title,
        verbose_name="Произведение",
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField(
        verbose_name="Текст комментария"
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации комментария",
        auto_now_add=True
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-pub_date"]
