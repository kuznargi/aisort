from django.db import models

# Create your models here.

class Test(models.Model):
      author=models.CharField(max_length=30)