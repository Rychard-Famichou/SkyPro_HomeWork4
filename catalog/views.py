from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ProductForm
from .models import ContactMessage, Product, Contact, Category


# Create your views here.
# def product_form(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         description = request.POST.get('description')
#         price = float(request.POST.get('price'))
#         category_id = request.POST.get('category')
#         category_instance = Category.objects.get(id=category_id)
#         Product.objects.create(
#             name=name,
#             description=description,
#             price=price,
#             category=category_instance
#         )
#         messages.success(request, f"Спасибо! Ваш продукт сохранен в базу данных.")
#         return redirect(request.path)
#     categories = Category.objects.all()
#     context = {"categories": categories}
#     return render(request, 'product_form.html', context=context)
def product_form(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Спасибо! Ваш продукт сохранен в базу данных.")
            return redirect(request.path)
    else:
        form = ProductForm()

    categories = Category.objects.all()

    context = {
        "categories": categories,
        "form": form
    }
    return render(request, 'product_form.html', context=context)


def product(request, product_id):
    one_product = Product.objects.get(id=product_id)
    context = {"product": one_product}
    return render(request, "catalog/product_detail.html", context=context)


def home(request):
    products = Product.objects.all()
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, 'catalog/home.html', context=context)


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
