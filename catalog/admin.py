from django.contrib import admin

from .models import ContactMessage


# Register your models here.

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    # Какие поля отображать в списке всех сообщений
    list_display = ('name', 'phone', 'created_at')

    # По каким полям можно искать (сверху появится строка поиска)
    search_fields = ('name', 'phone', 'message')

    # Фильтр справа по дате создания
    list_filter = ('created_at',)

    # Сортировка: сначала новые сообщения
    ordering = ('-created_at',)
    