from django.db import models
from django.db.models.signals import pre_save

# Create your models here.

class ConfigItem(models.Model):
    Key = models.CharField(max_length=128, unique=True)
    Value = models.TextField()
