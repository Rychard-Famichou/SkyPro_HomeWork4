from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('post_list/', views.PostListView.as_view(), name='post_list'),
    path('post_form/', views.PostCreateView.as_view(), name='post_form'),
    path('post_detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post_detail/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('post_detail/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)