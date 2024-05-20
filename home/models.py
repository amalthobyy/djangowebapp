from django.db import models

# Create your models here.

class userinfo (models.Model):
    username = models.CharField(max_length=30)
    Name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50,unique=True)

    
