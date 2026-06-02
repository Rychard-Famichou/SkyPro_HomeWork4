from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm  # <-- Подключаем форму создания
    form = CustomUserChangeForm  # <-- Подключаем форму редактирования
    # Поля, которые будут отображаться в списке пользователей
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')

    # Поля, по которым будет работать поиск
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # Фильтры в правой панели
    list_filter = ('is_superuser', 'is_staff', 'is_active')

    # Настройка сортировки (по умолчанию)
    ordering = ('username',)

    # Добавляем кастомные поля на страницу редактирования пользователя
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('bio', 'birth_date'),  # Укажите здесь ваши новые поля из models.py
        }),
    )

    # Добавляем кастомные поля на страницу создания нового пользователя (в админке)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('bio', 'birth_date'),
        }),
    )
