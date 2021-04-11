import threading
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from django.core.mail import EmailMessage
from .tasks import auth_email_task

class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))

account_activation_token = AppTokenGenerator()

def email_register(request,user,email_to):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))			
    domain = get_current_site(request).domain
    link = reverse(
        'activate',
        kwargs={
            'uidb64':uidb64,
            'token':account_activation_token.make_token(user)
        }
    )
    activate_url = f'http://{domain}{link}'
    email_subject = 'Activate your Ecommerce Website Account'
    email_body = f'Hi {user.username}. Please use this link to verify your account\n {activate_url}'
    fromEmail = 'noreply@ecommerce.com'
    auth_email_task.delay(email_subject,email_body,fromEmail,email_to)

class EmailThread(threading.Thread):
	def __init__(self,email):
		self.email = email
		threading.Thread.__init__(self)

	def run(self):
		self.email.send(fail_silently = False)