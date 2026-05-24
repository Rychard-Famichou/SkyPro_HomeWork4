from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import ContactMessage


# Create your views here.


def home(request):
    return render(request, 'catalog/home.html')

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Сохраняем данные в PostgreSQL одной строчкой!
        ContactMessage.objects.create(
            name=name,
            phone=phone,
            message=message
        )

        messages.success(request, f"Спасибо, {name}! Ваше сообщение сохранено в базу данных.")
        return redirect(request.path)

    return render(request, 'catalog/contacts.html')
