from django.db import models
from colorful.fields import RGBColorField

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length = 70)
    color = RGBColorField()

    def __str__(self):
        return self.name
