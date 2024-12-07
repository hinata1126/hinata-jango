from django.db import models 
from django.contrib.auth.models import User

class Category(models.Model): 
    name = models.CharField(max_length=255)

    def __str__(self):
         return self.name 

class Product(models.Model): 
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255) 
    description = models.TextField() 
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

# 1 はカテゴリ ID
    def __str__(self): 
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
