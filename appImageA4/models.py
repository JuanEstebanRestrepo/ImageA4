from django.db import models
from django.contrib.auth.models import User

class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    original_width = models.IntegerField(blank=False, null=False)
    original_height = models.IntegerField(blank=False, null=False)
    resize_width = models.IntegerField(blank=False, null=False)
    resize_height = models.IntegerField(blank=False, null=False)
