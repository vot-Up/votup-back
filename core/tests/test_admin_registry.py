"""Integration test: verify all ModelAdmins are registered (Task 06)."""

import pytest
from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from account.models import User
from core.admin import (
    CandidateAdmin,
    EventVotingAdmin,
    PlateAdmin,
    PlateUserAdmin,
    ResumeVoteAdmin,
    VoterAdmin,
    VotingPlateAdmin,
    VotingUserAdmin,
)
from core.models.models import Candidate, EventVoting, Plate, PlateUser, ResumeVote, Voter, VotingPlate, VotingUser


class TestCoreModelAdminRegistrations:
    """All 8 core models must have registered ModelAdmins."""

    def test_voter_registered(self):
        assert isinstance(admin.site._registry.get(Voter), VoterAdmin)

    def test_candidate_registered(self):
        assert isinstance(admin.site._registry.get(Candidate), CandidateAdmin)

    def test_plate_registered(self):
        assert isinstance(admin.site._registry.get(Plate), PlateAdmin)

    def test_plate_user_registered(self):
        assert isinstance(admin.site._registry.get(PlateUser), PlateUserAdmin)

    def test_event_voting_registered(self):
        assert isinstance(admin.site._registry.get(EventVoting), EventVotingAdmin)

    def test_voting_plate_registered(self):
        assert isinstance(admin.site._registry.get(VotingPlate), VotingPlateAdmin)

    def test_voting_user_registered(self):
        assert isinstance(admin.site._registry.get(VotingUser), VotingUserAdmin)

    def test_resume_vote_registered(self):
        assert isinstance(admin.site._registry.get(ResumeVote), ResumeVoteAdmin)


class TestSystemModelAdminRegistrations:
    """Account, auth, and authtoken models must be registered."""

    def test_user_registered(self):
        assert User in admin.site._registry

    def test_group_registered(self):
        assert Group in admin.site._registry

    def test_token_proxy_registered(self):
        assert TokenProxy in admin.site._registry


class TestTotalRegistrationCount:
    """Total registered models must cover core + system domains."""

    def test_total_registered_count(self):
        # 8 core + User + Group + TokenProxy = 11 minimum
        assert len(admin.site._registry) >= 11


@pytest.mark.django_db
class TestAdminIndexPage:
    @pytest.fixture
    def superuser(self, django_user_model):
        return django_user_model.objects.create_superuser(
            email="admin@registry-test.com",
            password="adminpass",
            name="Admin",
            cellphone="11988888888",
        )

    @pytest.fixture
    def admin_client(self, client, superuser):
        client.force_login(superuser)
        return client

    def test_admin_index_returns_200(self, admin_client):
        response = admin_client.get("/admin/")
        assert response.status_code == 200

    def test_core_changelist_pages_return_200(self, admin_client):
        urls = [
            "/admin/core/voter/",
            "/admin/core/candidate/",
            "/admin/core/plate/",
            "/admin/core/plateuser/",
            "/admin/core/eventvoting/",
            "/admin/core/votingplate/",
            "/admin/core/votinguser/",
            "/admin/core/resumevote/",
        ]
        for url in urls:
            response = admin_client.get(url)
            assert response.status_code == 200, f"{url} returned {response.status_code}"
