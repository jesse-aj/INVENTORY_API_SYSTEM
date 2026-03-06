from rest_framework import viewsets
from .models import InventoryItem, InventoryChangeLog
from .serializers import InventorySerializer, InventoryChangeLogSerializer


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventorySerializer


class InventoryChangeLogViewSet(viewsets.ModelViewSet):
    queryset = InventoryChangeLog.objects.all()
    serializer_class = InventoryChangeLogSerializer