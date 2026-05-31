from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import ProductForm
from .models import ContactMessage, Product, Contact, Category


# Create your views here.
class ProductMixin:
    model = Product
    context_object_name = 'product'

class ProductFormMixin(ProductMixin, SuccessMessageMixin):
    form_class = ProductForm
    template_name = 'product_form.html'

class ProductCreateView(ProductFormMixin, CreateView):
    success_message = "Товар «%(name)s» успешно добавлен в каталог!"

class ProductUpdateView(ProductFormMixin, UpdateView):
    success_message = "Данные товара «%(name)s» успешно обновлены."

class ProductDetailView(ProductMixin, DetailView):
    template_name = 'product_detail.html'

class ProductDeleteView(ProductMixin, SuccessMessageMixin, DeleteView):
    template_name = 'product_delete.html'
    success_url = reverse_lazy('catalog:home')
    success_message = "Товар был успешно удален из каталога."

class ProductListView(ProductMixin, ListView):
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 8
    def get_queryset(self):
        return Product.objects.all().order_by('-id')


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
