from django.urls import path
from .views import IndexView, product_detail, Menu_product, product_list, product_about

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('product/menu/', Menu_product.as_view(), name='menu' ),
    path('api/products/', product_list, name='product_list'),
    path("product/<slug:slug>/", product_about, name="product_about"),
]