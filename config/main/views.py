from django.http import HttpRequest
from django.shortcuts import render

from .models import Category, Product, ProductImage


def index(request: HttpRequest):
    category = Category.objects.all()
    product = Product.objects.all()
    product_image = ProductImage.objects.all()

    context = {
        "category": category,
        "product": product,
        "product_image": product_image,
    }

    return render(request,"index.html", context)


