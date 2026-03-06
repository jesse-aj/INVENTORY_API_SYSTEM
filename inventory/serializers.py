from rest_framework import serializers
from .models import InventoryItem, InventoryChangeLog

class InventorySerializer(serializers.ModelSerializer):
    


    class Meta:
        model = InventoryItem
        fields = "__all__"



class InventoryChangeLogSerializer(serializers.ModelSerializer):
    


    class Meta:
        model = InventoryChangeLog
        fields = "__all__"
