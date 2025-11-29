from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    img_url = models.CharField(max_length=250)
    name = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    url = models.CharField(max_length=250)
    datetime = models.DateTimeField(blank=True)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_content = models.CharField(max_length=250)
    post_time = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)