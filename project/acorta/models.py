from django.db import models

# Create your models here.

class Page(models.Model):
    url = models.TextField()
    shortened = models.IntegerField()
