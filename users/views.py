from django.contrib.auth import login
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm


# Create your views here.
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'  # Путь к HTML-шаблону
    success_url = reverse_lazy('catalog:home')    # Куда перенаправить после успешной регистрации

    def form_valid(self, form):
        # 1. Сохраняем нового пользователя в базу данных
        user = form.save()

        # 2. Автоматически авторизуем его в текущей сессии
        login(self.request, user)

        # 3. Перенаправляем на success_url
        return super().form_valid(form)
