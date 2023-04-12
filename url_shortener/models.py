from django.db import models
from django.utils import timezone

# Create your models here.

class short_url(models.Model):
    url = models.CharField(max_length=10000, unique= True)
    unique_url = models.CharField(max_length=10, primary_key= True)
    date = models.DateField(default=timezone.now())
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.unique_url