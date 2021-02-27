from django.conf import settings
from django.db import models

# Create your models here.
class Post(models.Model):
    DEFAULT = 'Default'
    TUX = 'Tux'
    DRAGON = 'Dragon'
    KITTY = 'Kitty'
    SKELETON = 'Skeleton'
    STATUS_CHOICES = [
        (DEFAULT, 'Default'),
        (TUX, 'Tux'),
        (DRAGON, 'Dragon'),
        (KITTY, 'Kitty'),
        (SKELETON, 'Skeleton'),
        ]
    text = models.CharField(max_length=100)
    cowsay_type = models.CharField(
        max_length=11,
        choices=STATUS_CHOICES,
        default=DEFAULT,)
    
    def __str__(self):
        return self.text