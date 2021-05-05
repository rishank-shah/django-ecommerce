import threading
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from django.core.mail import EmailMessage
from .tasks import auth_email_task
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail

class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (text_type(user.email_verified) + text_type(user.pk) + text_type(timestamp))

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
    email_body = f'Hi {user.username}. Please use the button below to verify your account'
    fromEmail = 'noreply@ecommerce.com'
    extra_info = f'''
                You are receving this mail because you registered on {domain}. 
                If you think this is a mistake, please contact the support team on {domain}.
                '''
    
    html_content = render_to_string("partials/_email_auth_template.html",{
        'email_title':'Verify Email Address',
        'email_body':email_body,
        'link_button':activate_url,
        'button_text':'Verify Account',
        'extra_info':extra_info,
    })
    text_content = strip_tags(html_content)
    # auth_email_task.delay(email_subject, text_content, fromEmail,email_to,html_content)
    EmailThread(email_subject, text_content, fromEmail,email_to,html_content).start()

class EmailThread(threading.Thread):

    def __init__(self,email_subject, text_content, fromEmail,to,html_content):
        self.email_subject = email_subject
        self.text_content = text_content
        self.fromEmail = fromEmail
        self.receiver = to
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.email_subject,
            self.text_content,
            self.fromEmail,
            [self.receiver],
            html_message = self.html_content
        )
        
def user_profile_pic_directory_path(instance, filename):
    return 'user_profile_pic/{0}/{1}'.format(instance.username ,filename)