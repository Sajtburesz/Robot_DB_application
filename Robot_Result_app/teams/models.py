from django.db import models
from django.conf import settings

class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_teams',null=False)
    maintainers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='maintainer', blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teams', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ["name","owner"]

    def __str__(self):
        return self.name

    
