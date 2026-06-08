from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
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


class ProductCreateView(ProductFormMixin, CreateView):
    success_message = "Товар «%(name)s» успешно добавлен в каталог!"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(UserPassesTestMixin, ProductFormMixin, UpdateView):
    success_message = "Данные товара «%(name)s» успешно обновлены."
    permission_required = 'catalog.change_product'
    login_url = 'users:home'

    def test_func(self):
        product = self.get_object()
        return product.owner == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для редактирования этого товара.")
        return redirect(self.login_url)


class ProductDetailView(ProductMixin, DetailView):
    template_name = 'catalog/product_detail.html'


class ProductDeleteView(UserPassesTestMixin, ProductMixin, SuccessMessageMixin, DeleteView):
    template_name = 'catalog/product_delete.html'
    success_url = reverse_lazy('catalog:product_list')
    success_message = "Товар был успешно удален из каталога."
    login_url = 'users:home'

    def test_func(self):
        user = self.request.user
        if user.has_perm('catalog.delete_product'):
            return True
        product = self.get_object()
        return product.owner == user

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для удаления этого товара.")
        return redirect(self.login_url)


class ProductListView(ProductMixin, ListView):
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self):
        queryset = Product.objects.all().order_by('-id')
        user = self.request.user
        # 1. Суперпользователь видит абсолютно всё
        if user.is_superuser:
            return queryset
        # 2. Модератор КАТАЛОГА (проверяем конкретное право на изменение продуктов)
        if user.has_perm('catalog.can_unpublish_product'):
            return queryset
        # 3. Авторизованный пользователь (обычный клиент / владелец товара / модератор БЛОГА)
        if user.is_authenticated:
            return queryset.filter(Q(is_published=True) | Q(owner=user))
        # 4. Анонимный гость
        return queryset.filter(is_published=True)


class ProductUnpublishView(PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save()
        return redirect('catalog:product_detail', pk=product.pk)


class ContactMessageCreateView(SuccessMessageMixin, CreateView):
    model = ContactMessage
    form_class = ContactMessageForm
    template_name = 'catalog/contacts.html'
    context_object_name = 'contact_message'
    success_url = reverse_lazy('catalog:home')
    success_message = f"Спасибо, «%(name)s»! Ваше сообщение сохранено в базу данных."
