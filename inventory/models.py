from django.db import models

# Create your models here.
class Inventory(models.Model):
    product = models.CharField(max_length=8)
    quantity = models.IntegerField()
    
