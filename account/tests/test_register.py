import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from account.serializers import RegisterSerializer
from core.models import models as core_models

pytestmark = pytest.mark.django_db

REGISTER_URL = "/api/account/register/"


def register_payload(**overrides):
    payload = {
        "name": "Registro Publico",
        "email": "registro.publico@test.com",
        "cellphone": "11970000001",
        "password": "testpass123",
        "confirm_password": "testpass123",
        "role": "ELEITOR",
    }
    payload.update(overrides)
    return payload


def post_register(payload):
    return APIClient().post(REGISTER_URL, payload, format="json")


def test_register_password_mismatch_returns_field_error():
    response = post_register(register_payload(confirm_password="different"))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "confirm_password" in response.data


def test_register_duplicate_email_returns_field_error(django_user_model):
    django_user_model.objects.create_user(
        email="duplicate-email@test.com",
        password="testpass123",
        cellphone="11970000002",
        name="Existing User",
    )

    response = post_register(register_payload(email="duplicate-email@test.com", cellphone="11970000003"))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data


def test_register_duplicate_cellphone_returns_field_error(django_user_model):
    django_user_model.objects.create_user(
        email="duplicate-cellphone@test.com",
        password="testpass123",
        cellphone="11970000004",
        name="Existing User",
    )

    response = post_register(register_payload(email="unique-cellphone@test.com", cellphone="11970000004"))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "cellphone" in response.data


def test_register_missing_role_returns_field_error():
    payload = register_payload()
    payload.pop("role")

    response = post_register(payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "role" in response.data


def test_register_invalid_role_returns_field_error():
    response = post_register(register_payload(role="INVALID"))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "role" in response.data


def test_register_serializer_valid_eleitor_creates_user_and_voter(django_user_model):
    serializer = RegisterSerializer(data=register_payload(email="eleitor@test.com", cellphone="11970000005"))
    assert serializer.is_valid(), serializer.errors

    user = serializer.save()

    assert django_user_model.objects.filter(email="eleitor@test.com", role="ELEITOR").exists()
    assert core_models.Voter.objects.filter(user=user, cellphone="11970000005").exists()
    assert not core_models.Candidate.objects.filter(user=user).exists()


def test_register_serializer_valid_candidato_creates_user_and_candidate(django_user_model):
    serializer = RegisterSerializer(
        data=register_payload(
            email="candidato@test.com",
            cellphone="11970000006",
            role="CANDIDATO",
        )
    )
    assert serializer.is_valid(), serializer.errors

    user = serializer.save()

    assert django_user_model.objects.filter(email="candidato@test.com", role="CANDIDATO").exists()
    assert core_models.Candidate.objects.filter(user=user, cellphone="11970000006").exists()
    assert not core_models.Voter.objects.filter(user=user).exists()


def test_register_endpoint_valid_eleitor_returns_201_with_access_token():
    response = post_register(register_payload(email="api-eleitor@test.com", cellphone="11970000007"))

    assert response.status_code == status.HTTP_201_CREATED
    assert "access" in response.data["token"]
    assert response.data["user"]["email"] == "api-eleitor@test.com"
    assert core_models.Voter.objects.filter(user__email="api-eleitor@test.com").exists()


def test_register_endpoint_valid_candidato_token_contains_role():
    response = post_register(
        register_payload(email="api-candidato@test.com", cellphone="11970000008", role="CANDIDATO")
    )

    assert response.status_code == status.HTTP_201_CREATED
    payload = AccessToken(response.data["token"]["access"]).payload
    assert payload["role"] == "CANDIDATO"
    assert core_models.Candidate.objects.filter(user__email="api-candidato@test.com").exists()


def test_register_endpoint_rolls_back_user_when_voter_creation_fails(django_user_model, monkeypatch):
    def fail_create(*args, **kwargs):
        raise RuntimeError("forced voter creation failure")

    monkeypatch.setattr(core_models.Voter.objects, "create", fail_create)
    client = APIClient()
    client.raise_request_exception = False

    response = client.post(
        REGISTER_URL,
        register_payload(email="rollback@test.com", cellphone="11970000009"),
        format="json",
    )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert not django_user_model.objects.filter(email="rollback@test.com").exists()


def test_register_endpoint_without_auth_header_is_allowed():
    response = post_register(register_payload(email="no-auth@test.com", cellphone="11970000010"))

    assert response.status_code == status.HTTP_201_CREATED
    assert "access" in response.data["token"]
