from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _



class User(AbstractUser):

    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_("email address"), unique=True)

    description = models.CharField(max_length=240, blank=True)
    avatar = models.CharField(max_length=255, default='default.png')

    REQUIRED_FIELDS = ["first_name","last_name","email"]

    def __str__(self):
        return self.username

    def owned_teams(self):
        return self.owned_teams.all()
    
    def member_teams(self):
        return self.teams.all()