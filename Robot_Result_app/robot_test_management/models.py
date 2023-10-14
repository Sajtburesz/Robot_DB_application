# from django.contrib.postgres.fields import JSONField
from django.db import models

class TestRun(models.Model):
    # attributes = JSONField()
    version = models.CharField(max_length=40)

class TestSuite(models.Model):
    name = models.CharField(max_length=255)
    test_run = models.ForeignKey(TestRun, on_delete=models.CASCADE)

class TestCase(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=[('Pass', 'Pass'), ('Fail', 'Fail')])
    suite = models.ForeignKey(TestSuite, on_delete=models.CASCADE)

class Keyword(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=[('Pass', 'Pass'), ('Fail', 'Fail')])
    log_message = models.TextField(null=True, blank=True)
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)