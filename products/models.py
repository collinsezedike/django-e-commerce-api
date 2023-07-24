from django.db import models


class Category(models.Model):
    category = models.CharField(max_length=50)
    class Meta:
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return self.category


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.FloatField()
    category = models.ManyToManyField(Category)
    
    def __str__(self):
        return self.name