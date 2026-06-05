from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import urlencode  # Импортируем для красивой сборки URL


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            return None

        login_url = reverse('users:login')

        if request.path == login_url:
            return None

        WHITE_LIST_NAMES = [
            'users:home',
            'users:register',
            'catalog:product_list',
            'blog:post_list',
            'catalog:contacts',
        ]

        current_route_name = request.resolver_match.view_name

        if current_route_name not in WHITE_LIST_NAMES:
            # 1. Формируем URL логина с параметром next.
            # Например, получится: /users/login/?next=/catalog/product/5/
            params = urlencode({'next': request.path})
            redirect_url = f"{login_url}?{params}"

            # 2. Перенаправляем пользователя на эту собранную ссылку
            return redirect(redirect_url)

        return None
