from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import ProductImage,Product
from django.contrib import messages
from .documents import ProductDocument
from django.conf import settings
from elasticsearch import Elasticsearch
from django.contrib import messages

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
            body = {
                "query" : {
                    "multi_match":{
                        "query" : search_item,
                        "type" : "phrase_prefix",
                        "fields" : [
                            'name',
                            'category',
                            'description'
                        ]
                    }
                }
            }
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
        products = Product.objects.all().order_by('-created_at')

    return render(request,'product/all_products.html',{
        'products': products
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
        