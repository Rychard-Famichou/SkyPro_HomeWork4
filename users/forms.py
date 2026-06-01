from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Список полей, которые будут видны при регистрации на сайте
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'birth_date')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        # Поля, которые пользователь сможет редактировать в своем профиле
        fields = ('first_name', 'last_name', 'bio', 'birth_date')
