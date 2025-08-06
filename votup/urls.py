from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path, reverse
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenRefreshView

from account.viewset import CustomTokenObtainPairView

urlpatterns = [
    path("", lambda request: redirect(reverse("api-root"))),
    path("admin/", admin.site.urls),
    # API URLs
    path("api/account/", include("account.urls")),
    path("api/account/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/account/refresh_token/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/votup/", include("core.urls"), name="api-root"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
