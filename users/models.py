from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    # Django уже имеет поля email, first_name, last_name в AbstractUser.
    # Здесь вы можете добавить любые свои уникальные поля:
    email = models.EmailField(unique=True, verbose_name="Почта")
    username = models.CharField(max_length=150, unique=False, blank=True, null=True, verbose_name="Никнейм")
    image = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name="Аватар")
    phone_number = models.CharField(max_length=11, blank=True, null=True, verbose_name="Телефон")
    country = models.CharField(max_length=11, blank=True, null=True, verbose_name="Страна")
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name="О себе")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Дата рождения")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
