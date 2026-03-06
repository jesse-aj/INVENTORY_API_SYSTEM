from rest_framework import routers
from .views import InventoryChangeLogViewSet, InventoryViewSet

router = routers.DefaultRouter()
router.register(r'inventory', InventoryViewSet)
router.register(r'changelog', InventoryChangeLogViewSet)

urlpatterns = router.urls
