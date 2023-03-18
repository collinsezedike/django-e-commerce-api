from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.FloatField()
    category = models.CharField(max_length=50, default="Uncategorized")
    
    def __str__(self):
        return self.name
