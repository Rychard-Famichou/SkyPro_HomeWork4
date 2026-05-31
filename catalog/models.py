from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


# Create your models here.
class Contact(models.Model):
    phone = models.CharField(max_length=20, verbose_name="Телефон, факс")
    email = models.EmailField(max_length=50, verbose_name="Электронная почта")
    address = models.TextField(verbose_name="Физический адрес для встреч и почты")

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    def __str__(self):
        return f"Сообщение от {self.name} ({self.created_at.strftime('%d.%m.%Y %H:%M')})"

    class Meta:
        verbose_name = 'Фидбэк'
        verbose_name_plural = 'Фидбэки'


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории", unique=True)
    description = models.TextField(verbose_name="Описание категории")

    def __str__(self):
        return f"Категория {self.name}."

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название продукта", unique=True)
    description = models.TextField(verbose_name="Описание продукта")
    image = models.ImageField(upload_to='photos/', verbose_name='Фотография продукта')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория продукта')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена продукта', validators=[MinValueValidator(0.01)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Продукт {self.name} из категории {self.category.name}. Цена {self.price}."

    def get_absolute_url(self):
        # Автоматически отправляет на страницу деталей созданного/измененного товара
        return reverse('catalog:product_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
