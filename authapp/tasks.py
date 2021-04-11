from celery import shared_task
from django.core.mail import EmailMessage

@shared_task
def auth_email_task(email_subject, email_body, fromEmail,email_to):
    email = EmailMessage(
        email_subject,
        email_body,
        fromEmail,
        [email_to],
    )
    email.send(
        fail_silently = False
    )

