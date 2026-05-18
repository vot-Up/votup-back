import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from account.serializers import CustomTokenObtainPairSerializer

pytestmark = pytest.mark.django_db


def create_role_user(django_user_model, role, suffix):
    return django_user_model.objects.create_user(
        email=f"{suffix}@jwt-role.test",
        password="testpass123",
        cellphone=f"1198888{suffix:0>4}",
        name=f"JWT Role {suffix}",
        role=role,
    )


def decoded_access_payload(user):
    refresh = CustomTokenObtainPairSerializer.get_token(user)
    return AccessToken(str(refresh.access_token)).payload


@pytest.mark.parametrize("role", ["ELEITOR", "CANDIDATO"])
def test_access_token_contains_user_role(django_user_model, role):
    user = create_role_user(django_user_model, role=role, suffix=role.lower())

    payload = decoded_access_payload(user)

    assert payload["role"] == role


def test_access_token_contains_null_role_for_admin(django_user_model):
    admin = django_user_model.objects.create_superuser(
        email="admin@jwt-role.test",
        password="testpass123",
        cellphone="11988880000",
        name="JWT Role Admin",
    )

    payload = decoded_access_payload(admin)

    assert payload["role"] is None


def test_access_token_preserves_existing_custom_fields(django_user_model):
    user = create_role_user(django_user_model, role="ELEITOR", suffix="fields")

    payload = decoded_access_payload(user)

    assert payload["user_id"] == user.id
    assert "username" in payload
    assert payload["email"] == user.email
    assert "user" in payload
    assert payload["role"] == "ELEITOR"


def test_token_endpoint_returns_access_token_with_role(django_user_model):
    user = create_role_user(django_user_model, role="ELEITOR", suffix="endpoint")
    client = APIClient()

    response = client.post(
        "/api/account/token/",
        {"email": user.email, "password": "testpass123"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    payload = AccessToken(response.data["token"]["access"]).payload
    assert payload["role"] == "ELEITOR"


def test_refresh_endpoint_returns_access_token_with_role(django_user_model):
    user = create_role_user(django_user_model, role="CANDIDATO", suffix="refresh")
    client = APIClient()
    login_response = client.post(
        "/api/account/token/",
        {"email": user.email, "password": "testpass123"},
        format="json",
    )

    response = client.post(
        "/api/account/refresh_token/",
        {"refresh": login_response.data["token"]["refresh"]},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    payload = AccessToken(response.data["access"]).payload
    assert payload["role"] == "CANDIDATO"
