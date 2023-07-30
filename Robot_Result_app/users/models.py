from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _



class User(AbstractUser):

    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_("email address"), unique=True)

    description = models.CharField(max_length=240, blank=True)
    avatar = models.ImageField(null=True, blank=True)

    REQUIRED_FIELDS = ["first_name","last_name","email"]

