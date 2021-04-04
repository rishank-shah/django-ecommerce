from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required(login_url='login')
def index(request):
    return HttpResponse('Logged in')