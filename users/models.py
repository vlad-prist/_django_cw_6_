from django.contrib.auth.models import AbstractUser
from django.db import models
from main.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True, **NULLABLE)
    token = models.CharField(max_length=100, verbose_name='token', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
