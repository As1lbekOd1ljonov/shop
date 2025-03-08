from django.db import models


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


    def __str__(self):
        return self.name

class ProductImage(models.Model):
    photo = models.ImageField(upload_to='product/image', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


    def __str__(self):
        return self.product.name
