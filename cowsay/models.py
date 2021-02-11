from django.conf import settings
from django.db import models
from django import forms

# Create your models here.
class Post(models.Model):
    text = models.CharField(max_length=200)
    
    def __str__(self):
        return self.text