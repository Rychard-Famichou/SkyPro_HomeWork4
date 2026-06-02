from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    # Django уже имеет поля email, first_name, last_name в AbstractUser.
    # Здесь вы можете добавить любые свои уникальные поля:
    bio = models.TextField(max_length=500, blank=True, verbose_name="О себе")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")

    def __str__(self):
        return f"{self.username} ({self.email})"
