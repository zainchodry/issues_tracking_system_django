from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):

    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MANAGER = "MANAGER", "Manager"
        DEVELOPER = "DEVELOPER", "Developer"

    email = models.EmailField(
        unique=True
    )

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.DEVELOPER
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "username"
    ]

    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    first_name = models.CharField(
        max_length=100,
        blank=True
    )

    last_name = models.CharField(
        max_length=100,
        blank=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    avatar = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True
    )

    address = models.CharField(
        max_length=255,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    country = models.CharField(
        max_length=100,
        blank=True
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.email} Profile"