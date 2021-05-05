"""ecommerce_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from products.views import all_products, price_filter
from products import views


urlpatterns = [
    path('',all_products,name="all_products"),
    path('price_filter/',price_filter,name="price_filter"),
    path('admin/', admin.site.urls),
    path('authentication/', include('authapp.urls')),
    path('profile/', include('authapp.profile_urls')),
    path('product/',include('products.urls')),
    path('cart/',include('products.cart_urls')),
]

admin.site.site_header = 'BART Ecommerce Admin'
admin.site.index_title = 'BART Ecommerce'
admin.site.site_title = 'BART Admin Site'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
