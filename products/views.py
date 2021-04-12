from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import ProductImage,Product
from django.contrib import messages
from .documents import ProductDocument
from django.conf import settings
from elasticsearch import Elasticsearch
from django.contrib import messages
from .search_query import search_product_query
from django.shortcuts import get_object_or_404


@login_required(login_url='login')
def index(request):
    return HttpResponse('Logged in')


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
                'count':len(data)
            })
        else:
            messages.error(request,'No Product found')
            return redirect('all_products')
    else:
        products = Product.objects.filter(
            is_draft=False
        ).order_by('-created_at')

    return render(request,'product/all_products.html',{
        'products': products
    })


def product_detail(request,slug):
    try:
        product = Product.objects.get(
            slug = slug,
            is_draft = False
        )
        return render(request,'product/product_detail.html',{
            'product':product
        })
    except Product.DoesNotExist:
        messages.error(request,'Something Went Wrong')
        return redirect('all_products')
        