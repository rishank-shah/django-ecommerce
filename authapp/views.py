from django.shortcuts import render,redirect
from django.views import View
from .models import User, UserAddress
from django.contrib import messages
from django.contrib import auth
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .utils import email_register,account_activation_token


class Registration(View):

    def get(self,request):
        return render(request,'authapp/register.html')

    def post(self,request):
        username = request.POST.get('u_name','')
        email = request.POST.get('email_1','')
        password = request.POST.get('password','')
        phone_number = request.POST.get('mobile_no','')
        first_name = request.POST.get('f_name','')
        last_name = request.POST.get('l_name','')

        context = {
            "username":username,
            "email":email,
            "last_name":last_name,
            "first_name":first_name,
            "phone_number":phone_number
        }

        list_context = list(context.values())
        if '' in list_context:
            messages.error(request,"All Fields are required")
            return render(request,'authapp/register.html',context=context)

        if not User.objects.filter(username=username).exists():
            if  not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request,'Password is too short')
                    return render(request,'authapp/register.html',context=context)
                
                user = User.objects.create_user(
                    username = username,
                    email = email,
                    first_name = first_name,
                    last_name = last_name,
                    phone_number = phone_number
                )
                user.set_password(password)
                user.is_active = True
                user.save()
                email_register(request,user,email)
                messages.success(request,'Account Created Succesfully. Please Confirm Email')
                return redirect('login')
            else:
                messages.error(request,'Email Already exists')
                return render(request,'authapp/register.html',context=context)
        else:
            messages.error(request,'Username Already exists')
            return render(request,'authapp/register.html',context=context)


class Login(View):

    def get(self,request):
        return render(request,'authapp/login.html')

    def post(self,request):
        username = request.POST.get('username','')
        password = request.POST.get('password','')

        context = {
            "username":username,
        }

        if username == '':
            messages.error(request,"Please Enter username")
            return render(request,'authapp/login.html',context=context)

        if password == '':
            messages.error(request,"Please Enter Password")
            return render(request,'authapp/login.html',context=context)

        if username and password:
            user = auth.authenticate(
                username = username,
                password = password
            )

            if user:
                auth.login(request,user)
                if not user.email_verified:
                    messages.error(request,'Please verify your email account.')
                messages.success(request,"Welcome, "+ user.username + ". You are now logged in.")
                return redirect('all_products')
            else:
                messages.error(request,'Invalid credentials')
                return render(request,'authapp/login.html',context=context)
        else:
            messages.error(request,'Something went wrong.')
            return render(request,'authapp/login.html',context=context)


class Logout(View):
	def post(self,request):
		auth.logout(request)
		messages.success(request,'Logged Out')
		return redirect('login')


class Verification(View):

	def get(self,request,uidb64,token):
        
		try:
			id = force_text(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=id)

			if not account_activation_token.check_token(user,token):
				messages.error(request,'Already Activated')
				return redirect('login')
			if user.email_verified:
				return redirect('login')
			user.email_verified = True
			user.save()
			messages.success(request,'Account activated Sucessfully')
			return redirect('login')
		except Exception as e:
			raise e
		return redirect('login')


def profile_details(request):

    if request.method == 'POST':
        username = request.user
        new_first_name = request.POST.get('first_name')
        new_last_name = request.POST.get('last_name')

        if User.objects.filter(username=username).exists():
            username.first_name = new_first_name,
            username.last_name = new_last_name
            username.save()
            messages.success(request,"Details updated successfully!")
            return render(request,'profile/profile_details.html')
            
        else:
            messages.error(request,"Something went wrong!")
            return render(request,'profile/profile_details.html')

    return render(request,'profile/profile_details.html')


def billing_details(request):
    return render(request,'profile/billing_details.html')


def shipping_details(request):
    if request.method == 'POST':
        username = request.user
        new_address = request.POST.get('flat_no') + request.POST.get('building_no') + request.POST.get('area')
        new_city = request.POST.get('city')
        new_state = request.POST.get('state')
        new_country = request.POST.get('country')
        new_zip_code = request.POST.get('zip_code')


        if User.objects.filter(username=username).exists():
            user_address = UserAddress.objects.create(user=username)
            user_address.address = new_address
            user_address.city = new_city
            user_address.state = new_state
            user_address.country = new_country
            user_address.zipcode = new_zip_code
            user_address.save()
            messages.success(request,"Address added successfully!")
            return render(request,'profile/profile_details.html')
            
        else:
            messages.error(request,"Something went wrong!")
            return render(request,'profile/profile_details.html')

    return render(request,'profile/shipping_detail.html')


def wishlist(request):
    return render(request,'profile/wishlist.html')


def change_email_pref(requst):
    pass