from django import forms
from django.core.exceptions import ValidationError
from .models import Product, ContactMessage


BAN_WORDS = ["казино", "крипта", "криптовалюта", "биржа", "дешево", "бесплатно", "обман", "полиция",
                     "радар"]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'description', 'image']
        error_messages = {
            'name': {
                'unique': "Продукт с таким названием уже существует в каталоге.",
            }
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',  # Добавление CSS-класса для стилизации поля
            'placeholder': 'Введите название продукта'  # Текст подсказки внутри поля
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',  # Добавление CSS-класса для стилизации поля
            'placeholder': 'Введите описание продукта'  # Текст подсказки внутри поля
        })
        self.fields['price'].widget.attrs.update({
            'class': 'form-control',  # Добавление CSS-класса для стилизации поля
            'placeholder': 'Введите цену продукта'  # Текст подсказки внутри поля
        })
        self.fields['category'].widget.attrs.update({
            'class': 'form-control',  # Добавление CSS-класса для стилизации поля
            'placeholder': 'Выберите категорию продукта'  # Текст подсказки внутри поля
        })
        self.fields['image'].widget.attrs.update({
            'class': 'form-control',  # Добавление CSS-класса для стилизации поля
            'placeholder': 'Загрузите изображение продукта'  # Текст подсказки внутри поля
        })

    def clean_image(self):
        image = self.cleaned_data['image']
        if image:
            max_size = 5 * 1024 * 1024
            if image.size > max_size:
                raise ValidationError("Размер файла не должен превышать 5 МБ.")

            allowed_extensions = ['jpg', 'jpeg', 'png']
            extension = image.name.split('.')[-1].lower()
            if extension not in allowed_extensions:
                raise ValidationError("Допускаются только файлы в формате JPEG или PNG.")

        return image

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError("Цена продукта не может быть отрицательной.")
        return price

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name').lower()
        description = cleaned_data.get('description').lower()
        for word in BAN_WORDS:
            if word in name:
                self.add_error('name', f"Название содержит запрещенное слово: '{word}'")
            if word in description:
                self.add_error('description', f"Описание содержит запрещенное слово: '{word}'")

        return cleaned_data


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'message']
        error_messages = {}
