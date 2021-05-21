from django.core.mail import send_mail
from django.template.loader import render_to_string



import random


def send_confirmation_code(user):
    print(f'From: hello@multivendor.io\nto: {user.email}\nConfirmation Code: {user.confirmation_code}')