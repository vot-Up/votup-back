from rest_framework.routers import DefaultRouter

from account import viewset

router = DefaultRouter()
router.register('user', viewset.UserViewSet)
urlpatterns = router.urls
