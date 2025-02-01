from api.constants import MAX_SLUG_CHAR, MAX_STRING_CHAR, MAX_STR_LENGTH
from django.db import models

from user.models import CustomUser
from reviews.validators import validate_year


class NameSlugModel(models.Model):
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
        abstract = True


class Genre(NameSlugModel):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(NameSlugModel):

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
        validators=[validate_year]
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

    def __str__(self):
        return self.name


class AuthorTextModel(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='%(class)s',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст')

    class Meta:
        abstract = True


class Review(AuthorTextModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
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
        return self.text[:MAX_STR_LENGTH]


class Comment(AuthorTextModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Обзор'
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
        return self.text[:MAX_STR_LENGTH]
