from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.template import Context, loader
from django.template.loader import render_to_string, get_template


from celery.decorators import task
from celery.utils.log import get_task_logger
from time import sleep


logger = get_task_logger(__name__)


@task(name='send_confirmation_mail')
def send_confirmation_mail(subject, new_user):
    sleep(10)
    mail_subject = subject
    context = {'new_user':new_user}
    message = loader.get_template('mail.html').render(context)
    to_email = new_user['email']
    from_email = 'hello@regnumchaplains.org'
    msg = EmailMessage(mail_subject, message, to=[to_email],from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()