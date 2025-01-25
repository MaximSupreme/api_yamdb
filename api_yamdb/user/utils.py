import secrets
import string
import re
from rest_framework import serializers
from django.conf import settings
from django.core.mail import send_mail


def customed_send_mail(email, confirmation_code):
    send_mail(
        'Your confirmation code',
        f'Your confirmation code: {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

def generate_confirmation_code():
    code = string.ascii_letters + string.digits
    return ''.join(secrets.choice(code) for _ in range(40))

def validate_username(value):
    if not re.match(r'^[\w.@+-]+$', value):
        raise serializers.ValidationError(
            '''Имя пользователя может содержать только буквы, 
            цифры и знаки @/./+/-/_'''
        )
    if value.lower() == 'me':
        raise serializers.ValidationError(
            'Имя пользователя "me" не разрешено'
        )
    return value
