from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from .forms import ProductForm, ContactMessageForm
from .models import ContactMessage, Product, Category
from .services import CatalogService


# Create your views here.
class CategoryMixin:
    model = Category
    context_object_name = 'category'


@method_decorator(cache_page(60 * 15), name='dispatch')
class CategoryDetailView(CategoryMixin, TemplateView):
    template_name = 'catalog/category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        category_id = self.request.GET.get('category_id')

        if category_id:
            try:
                current_category = get_object_or_404(Category, pk=category_id)
                context['current_category'] = current_category

                context['products'] = CatalogService.get_category_products(category_id)
            except Category.DoesNotExist:
                pass

        return context


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

    def get_object(self, queryset=None):
        # 1. Получаем ID товара из URL (Django сохраняет его в self.kwargs)
        product_id = self.kwargs.get(self.pk_url_kwarg) or self.kwargs.get('pk')
        # 2. Формируем свое собственное понятное имя ключа!
        cache_key = f'product_detail_{product_id}'
        # Модераторы всегда получают свежие данные из базы (без кэша)
        user = self.request.user
        is_moderator = user.is_superuser or user.has_perm('catalog.can_unpublish_product')
        if is_moderator:
            return super().get_object(queryset)
        # 3. Для обычных пользователей ищем в кэше
        product = cache.get(cache_key)
        if not product:
            # Если в кэше нет, берем из БД и сохраняем с красивым именем
            product = super().get_object(queryset)
            cache.set(cache_key, product, 60 * 15)
        if not product.is_published:
            raise Http404("Товар не опубликован или удален")
        return product


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
        # 1. Кэшируем только список ID
        product_ids = cache.get('productlist_ids')

        if not product_ids:
            # Получаем только ID из базы данных
            product_ids = list(Product.objects.all().order_by('-id').values_list('id', flat=True))
            cache.set('productlist_ids', product_ids, 60 * 15)

        # 2. Делаем ОДИН быстрый запрос к БД по закэшированным ID
        # Благодаря этому объекты "живые", пагинация и права работают идеально!
        queryset = Product.objects.filter(id__in=product_ids).order_by('-id')

        user = self.request.user

        # 3. Возвращаем обычный QuerySet с фильтрацией
        if user.is_superuser or user.has_perm('catalog.can_unpublish_product'):
            return queryset
        if user.is_authenticated:
            return queryset.filter(Q(is_published=True) | Q(owner=user))

        return queryset.filter(is_published=True)


class ProductUnpublishView(PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save()
        cache.delete(f'product_detail_{product.id}')
        return redirect('catalog:product_detail', pk=product.pk)


class ContactMessageCreateView(SuccessMessageMixin, CreateView):
    model = ContactMessage
    form_class = ContactMessageForm
    template_name = 'catalog/contacts.html'
    context_object_name = 'contact_message'
    success_url = reverse_lazy('catalog:home')
    success_message = f"Спасибо, «%(name)s»! Ваше сообщение сохранено в базу данных."
