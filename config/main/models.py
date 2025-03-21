from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model, SET_NULL
from django.db.models.lookups import GreaterThan
from django.template.defaulttags import comment


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    parents = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        if not self.parents:
            return self.name
        return f"{self.parents.name}: {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    price = models.IntegerField()
    discount = models.IntegerField(default=0)
    quantity = models.IntegerField(default=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    reyting = models.IntegerField(max_length=5)


    def __str__(self):
        return self.name

class ProductImage(models.Model):
    photo = models.ImageField(upload_to='product/image', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


    def __str__(self):
        return self.product.name


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.product.name}"



class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    discontinued = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=15, decimal_places=2)


    def __str__(self):
        return f'{self.user.username} {self.created}'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()


    def __str__(self):
        return f'{self.product.name}'


class City(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class DeliveryAddress(models.Model):
    order =models.ForeignKey(Order, on_delete=SET_NULL, null=True)
    name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=13)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=250)
    comment = models.CharField(max_length=1000, null=True, blank=True)
    delivered = models.BooleanField(default=False)

    def  __str__(self):
        return f'{self.name} {self.last_name}'