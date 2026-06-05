from django import forms
from django.core.exceptions import ValidationError
from django.forms import BooleanField

from .models import Product, ContactMessage


BAN_WORDS = ["казино", "крипта", "криптовалюта", "биржа", "дешево", "бесплатно", "обман", "полиция",
                     "радар"]


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field, in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

            if field.label and not isinstance(field, BooleanField):
                prefix = "Выберите" if hasattr(field.widget, 'choices') else "Введите"

                label_text = field.label.lower()
                if label_text:
                    label_text = label_text[0].lower() + label_text[1:]

                field.widget.attrs['placeholder'] = f"{prefix} {label_text}"
                

class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'description', 'image']
        error_messages = {
            'name': {
                'unique': "Продукт с таким названием уже существует в каталоге.",
            }
        }


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
