from django.db import models

class User(models.Model):
    Username = models.CharField(max_length=20)
    Password = models.CharField(max_length=32)
    Email =  models.CharField(max_length=50)
     
    def __str__(self):
        return f"Username: {self.Username}, Email: {self.Email}"