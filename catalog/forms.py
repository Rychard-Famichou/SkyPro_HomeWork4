from django import forms

from .models import Product, ContactMessage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'description']
        # Можно добавить Bootstrap-классы прямо сюда, если нужно
        error_messages = {
            'name': {
                'unique': "Продукт с таким названием уже существует в каталоге.",
            }
        }


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'message']
        error_messages = {}
