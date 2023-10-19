from django.db.models import JSONField
from django.db import models
from django.contrib.postgres.indexes import GinIndex

class Attributes(models.Model):
    key_name = models.CharField(max_length=255, unique=True)
    
class TestRun(models.Model):
    attributes = JSONField(blank=True,null=True)
    version = models.CharField(max_length=40)
    class Meta:
        indexes = [GinIndex(fields=['attributes'])]

class TestSuite(models.Model):
    name = models.CharField(max_length=255)
    test_run = models.ForeignKey(TestRun, on_delete=models.CASCADE)

class TestCase(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=[('Pass', 'Pass'), ('Fail', 'Fail')], null=True, blank=True)
    suite = models.ForeignKey(TestSuite, on_delete=models.CASCADE)

class Keyword(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=[('Pass', 'Pass'), ('Fail', 'Fail')], null=True, blank=True)
    log_message = models.TextField(null=True, blank=True)
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)