from django.contrib import admin
from .models import Product,ProductImage,Category,Company
from rangefilter.filter import DateTimeRangeFilter

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "get_category_name", 
        "get_company_name", 
        "price"
    )

    search_fields = [
        "name",
        "get_category_name", 
        "get_company_name"
    ]
 
    list_filter = [('created_at', DateTimeRangeFilter)]

    inlines = [ProductImageAdmin]

    def get_category_name(self,obj):
        return obj.category.category_name
    
    def get_company_name(self,obj):
        return obj.company.company_name
    class Meta:
       model = Product

admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(Company)
