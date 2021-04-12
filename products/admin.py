from django.contrib import admin
from .models import Product,ProductImage,Category,Company
from rangefilter.filter import DateTimeRangeFilter

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category_name", 
        "company_name", 
        "price"
    )

    search_fields = [
        "name",
        "category__category_name", 
        "company__company_name"
    ]
 
    list_filter = [
        ('created_at', DateTimeRangeFilter),
        'is_draft',
        'category__category_name',
        'company__company_name'
    ]

    inlines = [ProductImageAdmin]

    def category_name(self,obj):
        return obj.category.category_name
    
    def company_name(self,obj):
        return obj.company.company_name

    class Meta:
       model = Product

admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(Company)
