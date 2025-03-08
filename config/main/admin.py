from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Product, ProductImage


admin.site.register(ProductImage)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    list_display_links = ('name',)
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


class CommentInline(admin.TabularInline):
    model = ProductImage
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount', 'quantity')
    prepopulated_fields = {"slug": ("name",)}
    list_display_links = ('name',)
    inlines = [ProductImageInline, CommentInline]

    def get_image(self, product):
        image = product.images.all()
        if image:
            return mark_safe(f'<img src="{image[0].image.url}" width="100"')
        return 'image not available'