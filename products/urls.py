from django.urls import path
from . import views

urlpatterns = [
    path('check-login',views.index,name="check_login")
]
