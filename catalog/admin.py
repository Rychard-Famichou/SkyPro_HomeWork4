from django.contrib import admin

from .models import ContactMessage, Category, Product, Contact


# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'email', 'address',)
    search_fields = ('phone',)
    list_filter = ('address',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    # Какие поля отображать в списке всех сообщений
    list_display = ('name', 'phone', 'created_at',)
    # По каким полям можно искать (сверху появится строка поиска)
    search_fields = ('name', 'phone', 'message',)
    # Фильтр справа по дате создания
    list_filter = ('created_at',)
    # Сортировка: сначала новые сообщения
    ordering = ('-created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category',)
    search_fields = ('name', 'description',)
    list_filter = ('category',)
    ordering = ('name',)
