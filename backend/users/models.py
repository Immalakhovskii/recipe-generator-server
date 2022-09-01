from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ADMIN = 'admin'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (USER, 'User'),
    ]

    email = models.EmailField(
        verbose_name='Email',
        unique=True,
    )
    role = models.CharField(
        verbose_name='Role',
        max_length=50,
        choices=ROLES,
        default=USER)

    @property
    def is_admin(self):
        return self.role == self.ADMIN
