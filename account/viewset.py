# Create your views here.
from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from account import actions, exceptions, filters, messages, models, params_serializer, serializers
from core.schemas.schemas import AUTH_SCHEMAS, USER_SCHEMAS
from core.viewset import ViewSetBase, ViewSetPermissions


@extend_schema_view(reset_password=USER_SCHEMAS["reset_password"])
class UserViewSet(ViewSetBase, ViewSetPermissions):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    filterset_class = filters.UserFilter
    ordering = ("-id",)
    permission_classes_by_action = {"reset_password": (AllowAny,), "partial_update": (AllowAny,)}

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=["POST"])
    def reset_password(self, request, *args, **kwargs):
        param_serializer = params_serializer.ResetPasswordSerializerParams(data=request.data)
        param_serializer.is_valid(raise_exception=True)
        actions.UserActions.reset_password(**param_serializer.validated_data)
        return Response(data={"message": messages.VALID_PASSWORD}, status=status.HTTP_200_OK)


@extend_schema_view(post=AUTH_SCHEMAS["login"])
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            raise exceptions.InvalidCredentialsException

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
