from django.contrib import admin
from .models import *
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
        "company__company_name",
        "price"
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

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            min_price, max_price = search_term.split('-')
        except ValueError:
            pass
        else:
            queryset |= self.model.objects.filter(price__gte=min_price, price__lte=max_price)
        return queryset, use_distinct

    class Meta:
       model = Product


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'date_created',
        'completed'
    )

    search_fields = [
        'user',
        'date_created',
        'shipping_address',
        'transaction_id'
    ]

    list_filter = [
        ('date_created', DateTimeRangeFilter),
        'completed',
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'order',
        'quantity',
    )

    search_fields = [
        'product',
        'order',
        'date_added'
    ]

    list_filter = [
        ('date_added', DateTimeRangeFilter)
    ]




admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(Company)
