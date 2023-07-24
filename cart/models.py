from django.db import models
from django.core.validators import MinValueValidator

from customers.models import CustomerProfile
from products.models import Product


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.user.first_name}'s cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cart} - {self.quantity} {self.item}"
