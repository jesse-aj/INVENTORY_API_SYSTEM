from rest_framework import viewsets
from .models import InventoryItem, InventoryChangeLog
from .serializers import InventorySerializer, InventoryChangeLogSerializer
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated




class InventoryViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventorySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
           return [IsAuthenticated()]
        return [IsAuthenticated(),  IsOwner()]
    
    def update(self, request, *args, **kwargs):
        item = self.get_object()
        old_quantity = item.quantity  # save before update
        
        response = super().update(request, *args, **kwargs)  # perform the update
        
        item.refresh_from_db()  # get the updated item
    
        if old_quantity != item.quantity:  # only log if quantity changed
            InventoryChangeLog.objects.create(
                item=item,
                changed_by=request.user,
                old_quantity=old_quantity,
                new_quantity=item.quantity
        )
    
        return response
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InventoryChangeLogViewSet(viewsets.ModelViewSet):
    queryset = InventoryChangeLog.objects.all()
    serializer_class = InventoryChangeLogSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
           return [IsAuthenticated()]
        return [IsAuthenticated(),  IsOwner()]