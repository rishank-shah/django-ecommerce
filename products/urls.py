from django.urls import path
from . import views

urlpatterns = [
    path('check-login',views.index,name="check_login"),
    path('',views.all_products,name="all_products"),
    path('<slug>',views.product_detail,name="product_detail")
]
