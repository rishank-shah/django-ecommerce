from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from .forms import UserForm, UserProfileInfoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
import threading

# Create your views here.
def index(request):
    return render(request, 'authapp/index.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

def signupuser(request):
    if request.method == 'POST':
        form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            messages.success(request,"Registered Succesfully. Check Email for confirmation")
            # EmailThread(email).start()
            login(request,user)
            return redirect('index')

        else:
            print(form.errors,profile_form.errors)

    else:
        form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'authapp/signupuser.html',{'form':form, 'profile_form':profile_form})

def user_login (request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        if user:
            if user.is_active:
                login(request,user)
                # email = User.objects.get(username=username).email
                #
				# 	email_subject = 'You Logged into your Portal account'
				# 	email_body = "If you think someone else logged in. Please contact support or reset your password.\n\nYou are receving this message because you have enabled login email notifications in portal settings. If you don't want to recieve such emails in future please turn the login email notifications off in settings."
				# 	fromEmail = 'noreply@exam.com'
				# 	email = EmailMessage(
				# 		email_subject,
				# 		email_body,
				# 		fromEmail,
				# 		[email],
				# 	)
                return redirect('index')
            else:
                messages.error(request,'Account not Activated')
                return render(request,'authapp/loginuser.html', {'form':AuthenticationForm(), 'error':'Account not Activated.'})
        else:
            messages.error(request,"Invalid Login Details!")
            return render(request,'authapp/loginuser.html', {'form':AuthenticationForm(), 'error':'Invalid Login Details!'})
    else:
        messages.error(request,'Please fill all fields')
        return render(request,'authapp/loginuser.html', {'form':AuthenticationForm()})

class EmailThread(threading.Thread):
	def __init__(self,email):
		self.email = email
		threading.Thread.__init__(self)


	def run(self):
		self.email.send(fail_silently = False)


# def password_rest(request):
#     user = User.objects.get(username='john')
#     user.set_password('new password')
#     user.save()
