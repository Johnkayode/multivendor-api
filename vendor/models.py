from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


import uuid
import random


#Generate account confirmation code
def gen_confirmation_code():
    cc =  random.randrange(100000, 999999)
    
    try:
        user = CustomUser.objects.get(
            confirmation_code=cc
        )
        return gen_confirmation_code
    except CustomUser.DoesNotExist:
        return cc
    
    return cc




class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("email address cannot be left empty!"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("user_type", 'ADMIN')

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("superuser must set is_staff to True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("superuser must set is_superuser to True"))

        return self.create_user(email, password, **extra_fields)

        

class CustomUser(AbstractUser):

    USER_TYPE_CHOICES = (
      ('VENDOR', 'Vendor'),
      ('CUSTOMER', 'Customer'),
      ('ADMIN', 'Administrator')
    )

    username = None
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), blank=False, unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=15)
    is_confirmed = models.BooleanField(_("is confirmed"), default=False)
    confirmation_code = models.IntegerField(
        _("confirmation code"), default=gen_confirmation_code
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email




class Vendor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    shop_name = models.CharField(_("shop name"), blank=False, null=False, max_length=250
    )
    description = models.TextField(_("description"))
    phone_number = models.CharField(
        _("phone number"), blank=False, null=False, max_length=11
    )
    closed = models.BooleanField(default=True)
    suspended = models.BooleanField(default=False)

    def __str__(self):
        return self.shop_name
