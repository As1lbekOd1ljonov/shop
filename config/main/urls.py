from django.urls import path
from .views import index, product_detail

urlpatterns = [
    path('', index, name='home'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
]