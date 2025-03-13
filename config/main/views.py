from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect

from .form import CommentForm
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




@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comments = product.comments.all()
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            return redirect('product_detail', product_id=product.id)

    return render(request, 'product_detail.html', {'product': product, 'comments': comments, 'form': form})