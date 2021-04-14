from celery import shared_task
from django.core.mail import send_mail

@shared_task
def auth_email_task(email_subject, text_content, fromEmail,email_to,html_content):
    send_mail(email_subject, text_content, fromEmail,[email_to],html_message=html_content)

