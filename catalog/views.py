from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import ProductForm, ContactMessageForm
from .models import ContactMessage, Product


# Create your views here.
class ProductMixin:
    model = Product
    context_object_name = 'product'


class ProductFormMixin(ProductMixin, SuccessMessageMixin):
    form_class = ProductForm
    template_name = 'catalog/product_form.html'


class ProductCreateView(LoginRequiredMixin, ProductFormMixin, CreateView):
    success_message = "Товар «%(name)s» успешно добавлен в каталог!"


class ProductUpdateView(LoginRequiredMixin, ProductFormMixin, UpdateView):
    success_message = "Данные товара «%(name)s» успешно обновлены."


class ProductDetailView(LoginRequiredMixin, ProductMixin, DetailView):
    template_name = 'catalog/product_detail.html'


class ProductDeleteView(LoginRequiredMixin, ProductMixin, SuccessMessageMixin, DeleteView):
    template_name = 'catalog/product_delete.html'
    success_url = reverse_lazy('catalog:home')
    success_message = "Товар был успешно удален из каталога."


class ProductListView(ProductMixin, ListView):
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self):
        return Product.objects.all().order_by('-id')


class ContactMessageCreateView(SuccessMessageMixin, CreateView):
    model = ContactMessage
    form_class = ContactMessageForm
    template_name = 'catalog/contacts.html'
    context_object_name = 'contact_message'
    success_url = reverse_lazy('catalog:home')
    success_message = f"Спасибо, «%(name)s»! Ваше сообщение сохранено в базу данных."
