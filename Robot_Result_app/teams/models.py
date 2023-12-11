from django.db import models
from django.conf import settings

class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_teams',null=False)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='TeamMembership', related_name='teams', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class TeamMembership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_maintainer = models.BooleanField(default=False)

    class Meta:
        unique_together = ('team', 'user')
