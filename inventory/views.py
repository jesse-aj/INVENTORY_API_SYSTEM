from rest_framework import viewsets
from .models import InventoryItem, InventoryChangeLog
from .serializers import InventorySerializer, InventoryChangeLogSerializer
from .permissions import IsAdmin, IsStaffOrAdmin, IsViewerOrAbove
from rest_framework.permissions import IsAuthenticated


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventorySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated(), IsViewerOrAbove()]
        elif self.action == "destroy":
            return [IsAuthenticated(), IsAdmin()]
        else:
            return [IsAuthenticated(), IsStaffOrAdmin()]

    def update(self, request, *args, **kwargs):
        item = self.get_object()
        old_quantity = item.quantity

        response = super().update(request, *args, **kwargs)

        item.refresh_from_db()

        if old_quantity != item.quantity:
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
    http_method_names = ['get', 'head', 'options']

    def get_permissions(self):
        return [IsAuthenticated(), IsViewerOrAbove()]