from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'catalog'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.ProductListView.as_view(), name='home'),
    path('contacts/', views.ContactMessageCreateView.as_view(), name='contacts'),
    path('product_form/', views.ProductCreateView.as_view(), name='product_form'),
    path('product_detail/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product_detail/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_update'),
    path('product_detail/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    