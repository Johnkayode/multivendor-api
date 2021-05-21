from django.db import models
from django.utils.translation import gettext_lazy as _

from vendor.models import CustomUser

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(_("address"), blank=False, null=False, max_length=250
    )
    city = models.CharField(_("city"), blank=False, null=False, max_length=20
    )
    state = models.CharField(_("state"), blank=False, null=False, max_length=250
    )
    phone_number = models.CharField(
        _("phone number"), blank=False, null=False, max_length=11
    )

    def __str__(self):
        return self.user.email

        
