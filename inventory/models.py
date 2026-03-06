from django.db import models
from django.contrib.auth.models import User


CATEGORY_CHOICES = [
    ('electronics', 'Electronics'),
    ('clothing', 'Clothing'),
    ('food', 'Food'),
]

class InventoryItem(models.Model):
    name = models.CharField(max_length = 50)
    description = models.TextField(max_length=300)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
