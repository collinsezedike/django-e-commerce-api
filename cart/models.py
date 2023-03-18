from django.db import models
from customers.models import CustomerProfile
from products.models import Product


# Create your models here.
class CartItem(models.Model):
    user = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    

class Cart(models.Model):
    user = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    