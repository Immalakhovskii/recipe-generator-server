from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ADMIN = 'admin'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (USER, 'User'),
    ]
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    USERNAME_FIELD = 'email'

    email = models.EmailField(
        verbose_name='Email address',
        unique=True
    )

    role = models.CharField(
        verbose_name='Role',
        max_length=15,
        choices=ROLES,
        default=USER)

    @property
    def is_admin(self):
        return self.role == self.ADMIN
