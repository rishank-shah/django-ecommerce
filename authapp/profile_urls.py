from . import views
from django.urls import path

urlpatterns = [
    path('', views.profile_details,name='profile_details'),
    path('billing_details/',views.billing_details,name='billing_details'),
    path('shipping_details/',views.shipping_details,name='shipping_details'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('change_email_pref',views.change_email_pref,name='change_email_pref')
]