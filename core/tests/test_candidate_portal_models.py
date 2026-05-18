import pytest
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from core.models import models
from core.serializer.serializers import PlateSerializer

pytestmark = pytest.mark.django_db

PROFILE_EXISTING_BLANK_FIELD_EXCLUDES = ["avatar"]


def create_user(django_user_model, suffix, role="CANDIDATO"):
    return django_user_model.objects.create_user(
        email=f"user-{suffix}@test.com",
        password="testpass123",
        cellphone=f"1190001{suffix:04d}",
        name=f"User {suffix}",
        role=role,
    )


def serialize_plate(plate):
    request = Request(APIRequestFactory().get("/"))
    return PlateSerializer(plate, context={"request": request}).data


def test_plate_is_linked_returns_false_without_voting_plate():
    plate = models.Plate.objects.create(name="Chapa sem votacao")

    assert plate.is_linked is False


def test_plate_is_linked_returns_true_with_voting_plate():
    plate = models.Plate.objects.create(name="Chapa em votacao")
    voting = models.EventVoting.objects.create(description="Eleicao vinculada")
    models.VotingPlate.objects.create(plate=plate, voting=voting)

    assert plate.is_linked is True


def test_voter_user_null_is_valid_for_admin_created_record():
    voter = models.Voter.objects.create(name="Eleitor legado", cellphone="11999990001")

    voter.full_clean(exclude=PROFILE_EXISTING_BLANK_FIELD_EXCLUDES)

    assert voter.user is None


def test_candidate_user_null_is_valid_for_admin_created_record():
    candidate = models.Candidate.objects.create(name="Candidato legado", cellphone="11999990002")

    candidate.full_clean(exclude=PROFILE_EXISTING_BLANK_FIELD_EXCLUDES)

    assert candidate.user is None


def test_deleting_user_sets_voter_and_candidate_user_to_null(django_user_model):
    voter_user = create_user(django_user_model, 1, role="ELEITOR")
    candidate_user = create_user(django_user_model, 2)
    voter = models.Voter.objects.create(
        user=voter_user,
        name="Eleitor vinculado",
        cellphone="11999990003",
    )
    candidate = models.Candidate.objects.create(
        user=candidate_user,
        name="Candidato vinculado",
        cellphone="11999990004",
    )

    voter_user.delete()
    candidate_user.delete()
    voter.refresh_from_db()
    candidate.refresh_from_db()

    assert voter.user is None
    assert candidate.user is None


def test_plate_serializer_includes_is_linked_false_for_unlinked_plate():
    plate = models.Plate.objects.create(name="Chapa serializer livre")

    data = serialize_plate(plate)

    assert {"id", "url", "name", "active", "owner", "is_linked"}.issubset(data)
    assert data["name"] == plate.name
    assert data["is_linked"] is False


def test_plate_serializer_includes_is_linked_true_for_linked_plate():
    plate = models.Plate.objects.create(name="Chapa serializer vinculada")
    voting = models.EventVoting.objects.create(description="Eleicao serializer")
    models.VotingPlate.objects.create(plate=plate, voting=voting)

    data = serialize_plate(plate)

    assert data["is_linked"] is True
