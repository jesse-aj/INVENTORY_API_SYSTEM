from django.contrib import admin
from .models import InventoryItem, InventoryChangeLog

admin.site.register(InventoryItem)
admin.site.register(InventoryChangeLog)