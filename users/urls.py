from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import RegisterView, HomeView, UserLoginView, UserDetailView, UserUpdateView

app_name = 'users'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user_detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user_detail/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
]
