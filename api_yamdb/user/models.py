from django.db import models

from django.contrib.auth.models import AbstractUser

import uuid

from api.constants import ROLES, ROLE_USER, MAX_STRING_CHAR


class CustomUser(AbstractUser):
    username = models.CharField(max_length=MAX_STRING_CHAR, unique=True)
    email = models.EmailField(max_length=MAX_STRING_CHAR, unique=True)
    first_name = models.CharField(max_length=MAX_STRING_CHAR)
    last_name = models.CharField(max_length=MAX_STRING_CHAR)
    bio = models.CharField(max_length=MAX_STRING_CHAR)
    role = models.CharField(max_length=60, choices=ROLES, default=ROLE_USER)
    confirmation_code = models.CharField(max_length=MAX_STRING_CHAR, blank=True, null=True)
    REQUIRED_FIELDS = ('email',)
    
    def generate_confirmation_code(self):
        self.confirmation_code = str(uuid.uuid4())
        self.save()
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
