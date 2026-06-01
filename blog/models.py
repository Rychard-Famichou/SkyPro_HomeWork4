from django.db import models
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок", unique=True)
    content = models.TextField(verbose_name="Содержимое")
    image = models.ImageField(upload_to='photos/', verbose_name='Превью', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    views = models.IntegerField(default=0, verbose_name="Количество просмотров")

    def __str__(self):
        return f"Пост '{self.title}' с количеством просмотров: {self.views}"

    def get_absolute_url(self):
        # Автоматически отправляет на страницу деталей созданного/измененного товара
        return reverse('blog:post_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
