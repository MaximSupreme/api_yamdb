from django.contrib.auth.models import AbstractUser
from django.db import models

from api.constants import (MAX_LENGTH_FIRST_LAST_AND_USERNAME, MAX_STRING_CHAR,
                        ROLE_ADMIN, ROLE_MODERATOR, ROLE_USER, ROLES)


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=MAX_LENGTH_FIRST_LAST_AND_USERNAME, unique=True,
        verbose_name='Имя пользователя'
    )
    email = models.EmailField(
        max_length=MAX_STRING_CHAR, unique=True, verbose_name='Почта'
    )
    first_name = models.CharField(
        max_length=MAX_LENGTH_FIRST_LAST_AND_USERNAME, verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=MAX_LENGTH_FIRST_LAST_AND_USERNAME, verbose_name='Фамилия'
    )
    bio = models.CharField(
        max_length=MAX_STRING_CHAR, verbose_name='Биография'
    )
    role = models.CharField(
        max_length=60, choices=ROLES, default=ROLE_USER, verbose_name='Роль'
    )
    confirmation_code = models.CharField(
        max_length=MAX_STRING_CHAR, blank=True, null=True,
        verbose_name='Код подтверждения'
    )

    REQUIRED_FIELDS = ('email',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
    
    @property
    def is_admin(self):
        return self.role == ROLE_ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == ROLE_MODERATOR
