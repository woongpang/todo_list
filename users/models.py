from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    username = models.CharField(
        blank=True,
        null=True,
        max_length=15,
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        max_length=150,
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )
    age = models.PositiveIntegerField()
    introduction = models.TextField()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "age"]