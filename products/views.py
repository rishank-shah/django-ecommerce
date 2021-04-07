from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import ProductImage,Product
from django.contrib import messages

@login_required(login_url='login')
def index(request):
    return HttpResponse('Logged in')

def all_products(request):
    return render(request,'product/all_products.html',{
        'products':Product.objects.all().order_by('-timestamp')
    })

def product_detail(request,slug):
    if Product.objects.filter(slug = slug).exists():
        product = Product.objects.get(slug = slug)
        return render(request,'product/product_detail.html',{
            'product':product
        })
    else:
        messages.error(request,'Something Went Wrong')
        return redirect('all_products')
        