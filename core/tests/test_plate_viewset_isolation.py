import pytest
from rest_framework import status
from rest_framework.test import APIClient

from core.models import models

pytestmark = pytest.mark.django_db

PLATE_URL = "/api/votup/plate/"
PLATE_USER_URL = "/api/votup/plate_user/"


def make_user(django_user_model, suffix, role="CANDIDATO", is_staff=False, is_superuser=False):
    return django_user_model.objects.create_user(
        email=f"plate-{suffix}@test.com",
        password="testpass123",
        cellphone=f"1195000{suffix:04d}",
        name=f"Plate User {suffix}",
        role=role,
        is_staff=is_staff,
        is_superuser=is_superuser,
    )


def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


def response_results(response):
    if isinstance(response.data, dict) and "results" in response.data:
        return response.data["results"]
    return response.data


def create_candidate(suffix, user=None):
    return models.Candidate.objects.create(
        user=user,
        name=f"Candidate {suffix}",
        cellphone=f"1196000{suffix:04d}",
    )


def create_voting_plate(plate, description="Eleicao vinculada"):
    voting = models.EventVoting.objects.create(description=description)
    return models.VotingPlate.objects.create(plate=plate, voting=voting)


def test_admin_lists_all_plates(django_user_model):
    admin = make_user(django_user_model, 1, role=None, is_staff=True, is_superuser=True)
    owner = make_user(django_user_model, 2)
    own_plate = models.Plate.objects.create(name="Chapa do candidato", owner=owner)
    admin_plate = models.Plate.objects.create(name="Chapa administradora")

    response = auth_client(admin).get(PLATE_URL)

    assert response.status_code == status.HTTP_200_OK
    plate_ids = {item["id"] for item in response_results(response)}
    assert {own_plate.id, admin_plate.id}.issubset(plate_ids)


def test_candidate_lists_only_own_plate_and_excludes_admin_created_plates(django_user_model):
    candidate = make_user(django_user_model, 3)
    other_candidate = make_user(django_user_model, 4)
    own_plate = models.Plate.objects.create(name="Minha chapa", owner=candidate)
    models.Plate.objects.create(name="Chapa de outro candidato", owner=other_candidate)
    models.Plate.objects.create(name="Chapa sem dono")

    response = auth_client(candidate).get(PLATE_URL)

    assert response.status_code == status.HTTP_200_OK
    assert [item["id"] for item in response_results(response)] == [own_plate.id]


def test_candidate_create_sets_owner_to_request_user(django_user_model):
    candidate = make_user(django_user_model, 5)

    response = auth_client(candidate).post(PLATE_URL, {"name": "Chapa criada pela candidata"}, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    plate = models.Plate.objects.get(id=response.data["id"])
    assert plate.owner == candidate


def test_candidate_get_other_candidate_plate_returns_404(django_user_model):
    candidate = make_user(django_user_model, 6)
    other_candidate = make_user(django_user_model, 7)
    other_plate = models.Plate.objects.create(name="Chapa invisivel", owner=other_candidate)

    response = auth_client(candidate).get(f"{PLATE_URL}{other_plate.id}/")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_candidate_cannot_access_other_candidate_plate_with_mutating_methods(django_user_model):
    candidate = make_user(django_user_model, 8)
    other_candidate = make_user(django_user_model, 9)
    other_plate = models.Plate.objects.create(name="Chapa de outra pessoa", owner=other_candidate)
    client = auth_client(candidate)

    patch_response = client.patch(f"{PLATE_URL}{other_plate.id}/", {"name": "Tentativa"}, format="json")
    delete_response = client.delete(f"{PLATE_URL}{other_plate.id}/")

    assert patch_response.status_code == status.HTTP_404_NOT_FOUND
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND
    assert models.Plate.objects.filter(id=other_plate.id).exists()


def test_candidate_deletes_own_unlocked_plate(django_user_model):
    candidate = make_user(django_user_model, 10)
    plate = models.Plate.objects.create(name="Chapa removivel", owner=candidate)

    response = auth_client(candidate).delete(f"{PLATE_URL}{plate.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert not models.Plate.objects.filter(id=plate.id).exists()


def test_candidate_cannot_delete_own_locked_plate(django_user_model):
    candidate = make_user(django_user_model, 11)
    plate = models.Plate.objects.create(name="Chapa bloqueada", owner=candidate)
    create_voting_plate(plate)

    response = auth_client(candidate).delete(f"{PLATE_URL}{plate.id}/")

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data["detail"] == "Chapa em votação."
    assert models.Plate.objects.filter(id=plate.id).exists()


def test_candidate_plate_user_list_returns_only_members_from_own_plate(django_user_model):
    candidate = make_user(django_user_model, 12)
    other_candidate = make_user(django_user_model, 13)
    own_plate = models.Plate.objects.create(name="Chapa com membros", owner=candidate)
    other_plate = models.Plate.objects.create(name="Chapa com membros de outro", owner=other_candidate)
    own_member = models.PlateUser.objects.create(plate=own_plate, candidate=create_candidate(1), type="P")
    models.PlateUser.objects.create(plate=other_plate, candidate=create_candidate(2), type="P")

    response = auth_client(candidate).get(PLATE_USER_URL)

    assert response.status_code == status.HTTP_200_OK
    assert [item["id"] for item in response_results(response)] == [own_member.id]


def test_candidate_create_then_admin_links_then_candidate_patch_returns_403(django_user_model):
    candidate = make_user(django_user_model, 14)
    client = auth_client(candidate)
    create_response = client.post(PLATE_URL, {"name": "Chapa fluxo bloqueio"}, format="json")
    plate = models.Plate.objects.get(id=create_response.data["id"])
    create_voting_plate(plate, description="Eleicao fluxo bloqueio")

    response = client.patch(f"{PLATE_URL}{plate.id}/", {"name": "Chapa alterada"}, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN
    plate.refresh_from_db()
    assert plate.name == "Chapa fluxo bloqueio"


def test_admin_patch_locked_plate_succeeds(django_user_model):
    admin = make_user(django_user_model, 15, role=None, is_staff=True, is_superuser=True)
    plate = models.Plate.objects.create(name="Chapa bloqueada para admin")
    create_voting_plate(plate, description="Eleicao admin altera")

    response = auth_client(admin).patch(f"{PLATE_URL}{plate.id}/", {"name": "Chapa alterada pelo admin"}, format="json")

    assert response.status_code == status.HTTP_200_OK
    plate.refresh_from_db()
    assert plate.name == "Chapa alterada pelo admin"
