from .models import Post
from django import forms
from django.utils import timezone

class PostForm(forms.Form):
    
    class Meta:
        model = Post
        fields = ('text')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title