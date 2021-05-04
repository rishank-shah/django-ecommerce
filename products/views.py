from django.views.decorators.csrf import csrf_exempt
from products.cart import cartData, cookieCart, guest_user_cart
from authapp.models import User, UserAddress
import json
import datetime
from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import (
    Order,
    OrderItem,
    Product,
    ProductImage,
    Company,
    Category
)
from django.contrib import messages
from .documents import ProductDocument
from django.conf import settings
from elasticsearch import Elasticsearch
from django.contrib import messages
from .search_query import search_product_query
from django.shortcuts import get_object_or_404


def all_products(request):
    if 'q' in request.GET and hasattr(settings, "ELASTICSEARCH_DSL"):
        elastic_host = settings.ELASTICSEARCH_DSL["default"]["hosts"]
        es = Elasticsearch([f"http://{elastic_host}"])
        search_item = request.GET['q']
        products = es.search(
            index = 'product-index',
            body = search_product_query(search_item)
        )
        if len(products['hits']['hits']):
            data =  []
            results = products['hits']['hits']
            for i in results:
                data.append(i['_source'])
            return render(request,'product/all_products.html',{
                'products': data,
                'json':True,
                'categories':Category.objects.all(),
                'companies':Company.objects.all(),
                'count':len(data)
            })
        else:
            messages.error(request,'No Product found')
            return redirect('all_products')
    else:
        products = Product.objects.filter(
            is_draft=False
        ).order_by('-created_at')

    data = cartData(request)
    cartItems = data['cartItems']

    return render(request,'product/all_products.html',{
        'products': products,
        'companies':Company.objects.all(),
        'categories':Category.objects.all(),
        'cartItems':cartItems
    })


def product_detail(request,slug):
    try:
        products=Product.objects.all()[:4]
        product = Product.objects.get(
            slug = slug,
            is_draft = False
        )
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']

        return render(request,'product/product_detail.html',{
            'product':product,
            'cartItems':cartItems,
            'products' :products
        })

    except Product.DoesNotExist:
        messages.error(request,'Something Went Wrong')
        return redirect('all_products')
        

def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    orderitems = data['orderitems']


    context = {
        'orderitems':orderitems,
        'order':order,
        'cartItems':cartItems
    }
    return render(request, 'product/cart.html',context)


def update_item(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    print('Action:', action)
    print('Product:', productID)
    
    user = request.user
    product = Product.objects.get(id=productID)
    order, created = Order.objects.get_or_create(user=user, completed=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)


@csrf_exempt
def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, completed=False)
        total = float(data['orderInfo']['total'])
        order.transaction_id = transaction_id
        order.shipping_address = UserAddress.objects.get(id=data['orderInfo']['id'])

        if total == float(order.get_cart_total):
            order.completed = True
        order.save()
    
    else:
        print('User is not logged in!')

    return JsonResponse('Payment Complete',safe=False)


def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    orderitems = data['orderitems']

    if not request.user.is_authenticated:

        context = {
            'orderitems':orderitems,
            'order':order,
            'cartItems':cartItems
        }
        return render(request, 'product/checkout.html',context)

    email_verified = request.user.email_verified
    useraddress = data['useraddress']
    context = {
        'email_verified':email_verified,
        'useraddress':useraddress,
        'orderitems':orderitems,
        'order':order,
        'cartItems':cartItems
    }
    return render(request, 'product/checkout.html',context)


def cart_register(request):
    username = request.POST.get('inputName')
    email = request.POST.get('inputEmail')

    context = {
        'username':username,
        'email':email
    }
    return render(request, 'authapp/register.html',context)


def cart_login(request):
    username = request.POST.get('inputName')
    email = request.POST.get('inputEmail')

    context = {
        'username':username,
        'email':email
    }
    return render(request, 'authapp/login.html',context)