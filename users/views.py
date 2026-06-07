from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, DetailView

from blog.models import Post
from catalog.models import Product
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


# Create your views here.
class RegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'  # Путь к HTML-шаблону
    success_url = reverse_lazy('users:home')    # Куда перенаправить после успешной регистрации

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать в наш сервис'
        message = 'Спасибо, что зарегистрировались в нашем сервисе!'
        recipient_list = [user_email]
        send_mail(subject, message, None, recipient_list)


class HomeView(TemplateView):
    template_name = 'users/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['latest_product'] = Product.objects.filter(is_published=True).order_by('-pk').first()
        context['latest_post'] = Post.objects.filter(is_published=True).order_by('-pk').first()

        return context


class UserLoginView(LoginView):
    template_name = 'users/login.html'


class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'users/user_detail.html'
    context_object_name = 'user'


class UserUpdateView(FormView):
    form_class = CustomUserChangeForm
    template_name = 'users/user_update.html'
