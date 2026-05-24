from django.db import models

# Create your models here.


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    def __str__(self):
        return f"Сообщение от {self.name} ({self.created_at.strftime('%d.%m.%Y %H:%M')})"


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название продукта", unique=True)
    description = models.TextField(verbose_name="Описание продукта")

    def __str__(self):
        return f"Категория {self.name}."

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название продукта", unique=True)
    description = models.TextField(verbose_name="Описание продукта")
    image = models.ImageField(upload_to='photos/', verbose_name='Фотография продукта')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория продукта')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена продукта')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Продукт {self.name} из категории {self.category.name}. Цена {self.price}."

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']
