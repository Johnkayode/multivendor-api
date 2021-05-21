from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.template import Context, loader
from django.template.loader import render_to_string, get_template







def send_mail(subject, new_user, template):

    mail_subject = subject
    context = {'new_user':new_user}
    message = loader.get_template(template).render(context)
    to_email = new_user.email
    from_email = 'hello@multivendor.io'
    msg = EmailMessage(mail_subject, message, to=[to_email],from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()