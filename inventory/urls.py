from rest_framework import routers
from .views import InventoryChangeLogViewSet, InventoryViewSet
from users.views import UserViewSet



router = routers.DefaultRouter()
router.register(r'inventory', InventoryViewSet)
router.register(r'changelog', InventoryChangeLogViewSet)
router.register(r'users', UserViewSet)

urlpatterns = router.urls
