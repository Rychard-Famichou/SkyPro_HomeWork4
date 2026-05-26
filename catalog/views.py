from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import ContactMessage, Product, Contact


# Create your views here.
def home(request):
    latest_products = Product.objects.all().order_by("-created_at")[:5]
    print()
    for product in latest_products:
        print(product)
    print()
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

    # Получаем первую (и обычно единственную) запись с контактными данными из админки
    contact_data = Contact.objects.first()

    # Передаем её в шаблон под ключом 'contact'
    context = {"contact": contact_data}

    return render(request, "catalog/contacts.html", context)
