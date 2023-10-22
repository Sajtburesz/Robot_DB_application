from django.conf import settings
from django.db.models import JSONField
from django.db import models
from django.contrib.postgres.indexes import GinIndex

from teams.models import Team

class Attributes(models.Model):
    key_name = models.CharField(max_length=255, unique=True)
    
class TestRun(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE,related_name='test_runs')
    attributes = JSONField(blank=True,null=True)
    is_public = models.BooleanField(default=False)
    class Meta:
        indexes = [GinIndex(fields=['attributes'])]

class TestSuite(models.Model):
    name = models.CharField(max_length=255)
    test_run = models.ForeignKey(TestRun, on_delete=models.CASCADE, related_name='suites')

class TestCase(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, null=True, blank=True)
    suite = models.ForeignKey(TestSuite, on_delete=models.CASCADE,related_name='test_cases')

class Keyword(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, null=True, blank=True)
    doc = models.TextField(null=True, blank=True)
    log_message = models.TextField(null=True, blank=True)
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, related_name='keywords')

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    testrun = models.ForeignKey(TestRun, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)