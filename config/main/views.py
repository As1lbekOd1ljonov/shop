from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from .form import CommentForm
from .models import Category, Product, ProductImage


from django.shortcuts import render
from django.views.generic import ListView
from .models import Category, Product, ProductImage

class IndexView(ListView):
    template_name = "index.html"
    context_object_name = "products"
    model = Product

    def get_queryset(self):
        queryset = Product.objects.all()
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()

        product_images = {image.product_id: image.photo.url for image in ProductImage.objects.all()}
        context["product_images"] = product_images
        return context



class Menu_product(ListView):
    template_name = "menu.html"
    context_object_name = "products"
    model = Product

    def get_queryset(self):
        queryset = Product.objects.all()
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()

        product_images = {image.product_id: image.photo.url for image in ProductImage.objects.all()}
        context["product_images"] = product_images
        return context


def product_list(request):
    min_price = request.GET.get('min_price', 0)
    max_price = request.GET.get('max_price', 100000)

    products = Product.objects.filter(price__gte=min_price, price__lte=max_price)
    data = list(products.values('id', 'name', 'price'))

    return JsonResponse(data, safe=False)




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


def product_about(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        "product": product
    }
    return render(request, "about.html", context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': 1
        }

    request.session['cart'] = cart
    request.session.modified = True

    return JsonResponse({'message': 'Product added to cart', 'cart': cart})

