from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms import BooleanField
from django.urls import reverse_lazy
from django.views import View

from .models import CustomUser


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field, in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class CustomUserCreationForm(StyleFormMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Список полей, которые будут видны при регистрации на сайте
        fields = ('email',)


class CustomUserChangeForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = CustomUser
        # Поля, которые пользователь сможет редактировать в своем профиле
        fields = ('first_name', 'last_name', 'image', 'phone_number', 'country', 'bio', 'birth_date')

class CustomAuthenticationForm(AuthenticationForm):
    pass
