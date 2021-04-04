from django.urls import path
from .views import Registration,Login,Logout,Verification
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('register/',Registration.as_view(),name = 'register'),
    path('login/', Login.as_view(), name="login"), 
    path('activate-account/<uidb64>/<token>',Verification.as_view(),name = 'activate'),
    path('logout', Logout.as_view(), name="logout"), 
]
