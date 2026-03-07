from rest_framework import viewsets
from .models import InventoryItem, InventoryChangeLog
from .serializers import InventorySerializer, InventoryChangeLogSerializer
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated




class InventoryViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventorySerializer


class InventoryChangeLogViewSet(viewsets.ModelViewSet):
    queryset = InventoryChangeLog.objects.all()
    serializer_class = InventoryChangeLogSerializer


    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
           return [IsAuthenticated()]
        return [IsAuthenticated(),  IsOwner()]