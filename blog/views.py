from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.core.mail import send_mail
from django.db.models import F
from blog.forms import PostForm
from blog.models import Post


# Create your views here.
class PostMixin:
    model = Post
    context_object_name = 'post'


class PostFormMixin(PostMixin, SuccessMessageMixin):
    form_class = PostForm
    template_name = 'blog/post_form.html'


class PostListView(PostMixin, ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.filter(is_published=True).order_by('-id')


class PostCreateView(PostFormMixin, CreateView):
    success_message = "Пост «%(title)s» успешно добавлен."


class PostUpdateView(UserPassesTestMixin, PostFormMixin, UpdateView):
    success_message = "Пост «%(title)s» успешно обновлён."
    permission_required = 'blog.change_post'
    login_url = 'users:home'

    def test_func(self):
        return self.request.user.has_perm('blog.change_post')

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для редактирования постов.")
        return redirect(self.login_url)


class PostDetailView(PostMixin, DetailView):
    template_name = 'blog/post_detail.html'

    queryset = Post.objects.select_related('user')

    def get_object(self, queryset=None):
        # Передаем наш оптимизированный queryset в родительский метод
        if queryset is None:
            queryset = self.get_queryset()

        obj = super().get_object(queryset)

        # Обновляем просмотры в базе данных
        Post.objects.filter(pk=obj.pk).update(views=F('views') + 1)
        # Загружаем свежие данные из базы
        obj.refresh_from_db()
        # Проверяем условие
        if obj.views == 100:
            author_email = obj.user.email
            if author_email:
                send_mail(
                    subject='Поздравляем! Ваш пост набрал 100 просмотров',
                    message=f'Пост "{obj.title}" набрал 100 просмотров!',
                    from_email='rychard.famichou@gmail.com',  # Должен совпадать с EMAIL_HOST_USER
                    recipient_list=[author_email],  # Личная почта получателя
                    fail_silently=False,  # Поменяйте на False на время тестов, чтобы видеть ошибки, если они будут
                )
        return obj


class PostDeleteView(UserPassesTestMixin, PostMixin, SuccessMessageMixin, DeleteView):
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('blog:post_list')
    success_message = "Пост «%(title)s» был успешно удален."
    permission_required = 'blog.delete_post'
    login_url = 'users:home'

    def test_func(self):
        return self.request.user.has_perm('blog.delete_post')

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для удаления постов.")
        return redirect(self.login_url)
