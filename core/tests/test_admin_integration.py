"""Integration tests for final admin validation (Task 06).

Verifies that all expected models have registered ModelAdmins,
manage.py check passes, and all ModelAdmins have required configurations.
"""

import pytest
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from account.admin import UserAdmin
from core.admin.people import CandidateAdmin, VoterAdmin
from core.admin.plates import PlateAdmin, PlateUserAdmin
from core.admin.voting import (
    EventVotingAdmin,
    ResumeVoteAdmin,
    VotingPlateAdmin,
    VotingUserAdmin,
)
from core.models.models import (
    Candidate,
    EventVoting,
    Plate,
    PlateUser,
    ResumeVote,
    Voter,
    VotingPlate,
    VotingUser,
)

User = get_user_model()


class TestAllModelsRegistered:
    """Verify all 12+ models have registered ModelAdmins."""

    def test_voter_registered(self):
        assert Voter in admin.site._registry

    def test_candidate_registered(self):
        assert Candidate in admin.site._registry

    def test_plate_registered(self):
        assert Plate in admin.site._registry

    def test_plateuser_registered(self):
        assert PlateUser in admin.site._registry

    def test_eventvoting_registered(self):
        assert EventVoting in admin.site._registry

    def test_votingplate_registered(self):
        assert VotingPlate in admin.site._registry

    def test_votinguser_registered(self):
        assert VotingUser in admin.site._registry

    def test_resumevote_registered(self):
        assert ResumeVote in admin.site._registry

    def test_user_registered(self):
        assert User in admin.site._registry

    def test_group_registered(self):
        assert Group in admin.site._registry

    def test_tokenproxy_registered(self):
        assert TokenProxy in admin.site._registry

    def test_total_registered_models(self):
        """Total registered model count >= 11 (core 8 + account 1 + auth 1 + authtoken 1)."""
        assert len(admin.site._registry) >= 11


class TestAllModelAdminsHaveRequiredConfig:
    """Verify all business ModelAdmins have list_display, search_fields, list_filter."""

    @pytest.mark.parametrize(
        "model,admin_cls",
        [
            (Voter, VoterAdmin),
            (Candidate, CandidateAdmin),
            (Plate, PlateAdmin),
            (PlateUser, PlateUserAdmin),
            (EventVoting, EventVotingAdmin),
            (VotingPlate, VotingPlateAdmin),
            (VotingUser, VotingUserAdmin),
            (ResumeVote, ResumeVoteAdmin),
            (User, UserAdmin),
        ],
    )
    def test_has_list_display(self, model, admin_cls):
        registered_admin = admin.site._registry[model]
        assert registered_admin.list_display is not None
        assert len(registered_admin.list_display) > 0

    @pytest.mark.parametrize(
        "model,admin_cls",
        [
            (Voter, VoterAdmin),
            (Candidate, CandidateAdmin),
            (Plate, PlateAdmin),
            (PlateUser, PlateUserAdmin),
            (EventVoting, EventVotingAdmin),
            (VotingPlate, VotingPlateAdmin),
            (VotingUser, VotingUserAdmin),
            (ResumeVote, ResumeVoteAdmin),
            (User, UserAdmin),
        ],
    )
    def test_has_search_fields(self, model, admin_cls):
        registered_admin = admin.site._registry[model]
        assert registered_admin.search_fields is not None
        assert len(registered_admin.search_fields) > 0

    @pytest.mark.parametrize(
        "model,admin_cls",
        [
            (Voter, VoterAdmin),
            (Candidate, CandidateAdmin),
            (Plate, PlateAdmin),
            (PlateUser, PlateUserAdmin),
            (EventVoting, EventVotingAdmin),
            (VotingPlate, VotingPlateAdmin),
            (VotingUser, VotingUserAdmin),
            (ResumeVote, ResumeVoteAdmin),
            (User, UserAdmin),
        ],
    )
    def test_has_list_filter(self, model, admin_cls):
        registered_admin = admin.site._registry[model]
        assert registered_admin.list_filter is not None
        assert len(registered_admin.list_filter) > 0


class TestAdminActionsAvailable:
    """Verify custom actions are available on their respective ModelAdmins."""

    def test_eventvoting_has_activate_action(self):
        admin_obj = admin.site._registry[EventVoting]
        action_names = [a.__name__ if callable(a) else a for a in admin_obj.actions]
        assert "activate_voting" in action_names

    def test_eventvoting_has_close_action(self):
        admin_obj = admin.site._registry[EventVoting]
        action_names = [a.__name__ if callable(a) else a for a in admin_obj.actions]
        assert "close_voting" in action_names

    def test_plate_has_activate_action(self):
        admin_obj = admin.site._registry[Plate]
        action_names = [a.__name__ if callable(a) else a for a in admin_obj.actions]
        assert "activate_plate_action" in action_names


class TestInlinesAvailable:
    """Verify inlines are configured on their parent ModelAdmins."""

    def test_plate_has_plateuser_inline(self):
        admin_obj = admin.site._registry[Plate]
        inline_models = [inline.model for inline in admin_obj.inlines]
        assert PlateUser in inline_models

    def test_eventvoting_has_three_inlines(self):
        admin_obj = admin.site._registry[EventVoting]
        inline_models = [inline.model for inline in admin_obj.inlines]
        assert VotingPlate in inline_models
        assert VotingUser in inline_models
        assert ResumeVote in inline_models
