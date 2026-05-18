from rest_framework.routers import DefaultRouter

from account import viewset

router = DefaultRouter()
router.register("register", viewset.RegisterViewSet, basename="register")
router.register("user", viewset.UserViewSet)
urlpatterns = router.urls
