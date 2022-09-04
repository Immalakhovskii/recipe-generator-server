from django.db import models
from django.db.models import Q, F
from django.contrib.auth.models import AbstractUser
from django.db.models.constraints import UniqueConstraint, CheckConstraint


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

    def __str__(self):
        return self.username


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Subscriber',
    )
    subscription = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name='Subscription',
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['subscriber', 'subscription'],
                name='unique_subscription',
            ),
            CheckConstraint(
                check=Q(_negated=True, subscriber=F('subscription')),
                name='self_subscription',
            ),
        ]

    def __str__(self):
        return f'{self.subscriber} subscribed to {self.subscription}'
