from django.contrib import admin
from .models import Product,ProductImage

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

    class Meta:
       model = Product

admin.site.register(ProductImage)
