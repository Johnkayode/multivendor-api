from django.db import models
from django.utils.translation import gettext_lazy as _

from vendor.models import CustomUser

class Administrator(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(
        _("phone number"), blank=False, null=False, max_length=11
    )

    def __str__(self):
        return self.user.email
