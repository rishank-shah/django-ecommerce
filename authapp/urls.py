from django.urls import path
from . import views

app_name = "authapp"

urlpatterns = [
    path('signup/', views.signupuser, name='signupuser'),
    path('user_login/',views.user_login,name='user_login')
]
