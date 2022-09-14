from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Q
from django.db.models.constraints import CheckConstraint, UniqueConstraint


class CustomUser(AbstractUser):
    ADMIN = 'admin'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (USER, 'User'),
    ]
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    USERNAME_FIELD = 'email'

    email = models.EmailField(
        verbose_name='email address',
        unique=True
    )
    first_name = models.CharField(
        verbose_name='first name',
        max_length=150,
        blank=False
    )
    last_name = models.CharField(
        verbose_name='last name',
        max_length=150,
        blank=False
    )
    role = models.CharField(
        verbose_name='role',
        max_length=15,
        choices=ROLES,
        default=USER)

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    def __str__(self):
        return f'{self.first_name} {self.username}'


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='subscriber',
    )
    subscription = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name='subscription',
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['subscriber', 'subscription'],
                name='subscription must be unique',
            ),
            CheckConstraint(
                check=Q(_negated=True, subscriber=F('subscription')),
                name='self subscription prohibited',
            ),
        ]

    def __str__(self):
        return f'{self.subscriber} subscribed to {self.subscription}'
