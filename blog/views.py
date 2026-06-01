from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
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


class PostUpdateView(PostFormMixin, UpdateView):
    success_message = "Пост «%(title)s» успешно обновлён."


class PostDetailView(PostMixin, DetailView):
    template_name = 'blog/post_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        Post.objects.filter(pk=obj.pk).update(views=F('views') + 1)
        obj.views += 1
        return obj


class PostDeleteView(PostMixin, SuccessMessageMixin, DeleteView):
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('blog:post_list')
    success_message = "Пост «%(title)s» был успешно удален."
