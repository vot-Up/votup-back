"""Unit tests for core/admin/voting.py (Task 04)."""

from unittest.mock import MagicMock, patch

import pytest
from django.contrib import admin
from django.contrib.messages import ERROR

from core.admin.voting import (
    EventVotingAdmin,
    ResumeVoteAdmin,
    ResumeVoteInline,
    VotingPlateAdmin,
    VotingPlateInline,
    VotingUserAdmin,
    VotingUserInline,
)
from core.models.models import EventVoting, ResumeVote, VotingPlate, VotingUser


class TestAdminRegistrations:
    def test_event_voting_admin_registered(self):
        assert isinstance(admin.site._registry.get(EventVoting), EventVotingAdmin)

    def test_voting_plate_admin_registered(self):
        assert isinstance(admin.site._registry.get(VotingPlate), VotingPlateAdmin)

    def test_voting_user_admin_registered(self):
        assert isinstance(admin.site._registry.get(VotingUser), VotingUserAdmin)

    def test_resume_vote_admin_registered(self):
        assert isinstance(admin.site._registry.get(ResumeVote), ResumeVoteAdmin)


class TestEventVotingAdminInlines:
    def test_voting_plate_inline_in_event_voting_admin(self):
        assert VotingPlateInline in EventVotingAdmin.inlines

    def test_voting_user_inline_in_event_voting_admin(self):
        assert VotingUserInline in EventVotingAdmin.inlines

    def test_resume_vote_inline_in_event_voting_admin(self):
        assert ResumeVoteInline in EventVotingAdmin.inlines

    def test_all_inlines_have_tab_true(self):
        for inline_cls in [VotingPlateInline, VotingUserInline, ResumeVoteInline]:
            assert inline_cls.tab is True, f"{inline_cls.__name__}.tab should be True"


class TestUnfoldAdminConfig:
    @pytest.mark.parametrize(
        "admin_cls",
        [EventVotingAdmin, VotingPlateAdmin, VotingUserAdmin, ResumeVoteAdmin],
    )
    def test_compressed_fields(self, admin_cls):
        assert admin_cls.compressed_fields is True

    @pytest.mark.parametrize(
        "admin_cls",
        [EventVotingAdmin, VotingPlateAdmin, VotingUserAdmin, ResumeVoteAdmin],
    )
    def test_warn_unsaved_form(self, admin_cls):
        assert admin_cls.warn_unsaved_form is True


class TestEventVotingAdminConfig:
    def test_list_display(self):
        assert EventVotingAdmin.list_display == ("description", "date", "active", "created_at")

    def test_search_fields(self):
        assert EventVotingAdmin.search_fields == ("description",)

    def test_list_filter(self):
        assert EventVotingAdmin.list_filter == ("active",)


class TestVotingPlateAdminConfig:
    def test_list_display(self):
        assert VotingPlateAdmin.list_display == ("voting", "plate", "active", "created_at")

    def test_search_fields(self):
        assert VotingPlateAdmin.search_fields == ("voting__description", "plate__name")

    def test_list_filter(self):
        assert VotingPlateAdmin.list_filter == ("active",)


class TestVotingUserAdminConfig:
    def test_list_display(self):
        assert VotingUserAdmin.list_display == ("voting", "voter", "plate", "active", "created_at")

    def test_search_fields(self):
        assert VotingUserAdmin.search_fields == ("voting__description", "voter__name", "plate__name")

    def test_list_filter(self):
        assert VotingUserAdmin.list_filter == ("active",)


class TestResumeVoteAdminConfig:
    def test_list_display(self):
        assert ResumeVoteAdmin.list_display == ("voting", "plate", "quantity", "active", "created_at")

    def test_search_fields(self):
        assert ResumeVoteAdmin.search_fields == ("voting__description", "plate__name")

    def test_list_filter(self):
        assert ResumeVoteAdmin.list_filter == ("active",)


@pytest.mark.django_db
class TestActivateVotingAction:
    def _make_admin(self):
        return EventVotingAdmin(EventVoting, admin.site)

    def _make_request(self):
        request = MagicMock()
        request._messages = MagicMock()
        return request

    def _make_event(self, event_id=1, description="Test Voting"):
        event = MagicMock(spec=EventVoting)
        event.id = event_id
        event.description = description
        return event

    def test_action_calls_service_with_event_id(self):
        event_admin = self._make_admin()
        request = self._make_request()
        event = self._make_event(event_id=10)
        queryset = [event]

        with patch("core.admin.voting.voting_service.active_vote") as mock_activate:
            with patch.object(event_admin, "message_user"):
                event_admin.activate_voting(request, queryset)

        mock_activate.assert_called_once_with(10)

    def test_action_success_message_on_success(self):
        event_admin = self._make_admin()
        request = self._make_request()
        event = self._make_event(description="Eleição 2025")
        queryset = [event]

        with patch("core.admin.voting.voting_service.active_vote"):
            with patch.object(event_admin, "message_user") as mock_msg:
                event_admin.activate_voting(request, queryset)

        mock_msg.assert_called_once_with(request, "Votação 'Eleição 2025' ativada.")

    def test_action_error_message_on_service_exception(self):
        event_admin = self._make_admin()
        request = self._make_request()
        event = self._make_event()
        queryset = [event]

        with patch(
            "core.admin.voting.voting_service.active_vote",
            side_effect=Exception("já existe votação ativa"),
        ):
            with patch.object(event_admin, "message_user") as mock_msg:
                event_admin.activate_voting(request, queryset)

        mock_msg.assert_called_once_with(request, "já existe votação ativa", level=ERROR)

    def test_action_logs_error_on_exception(self):
        event_admin = self._make_admin()
        request = self._make_request()
        event = self._make_event(event_id=5)
        queryset = [event]

        with patch("core.admin.voting.voting_service.active_vote", side_effect=Exception("fail")):
            with patch.object(event_admin, "message_user"):
                with patch("core.admin.voting.logger") as mock_logger:
                    event_admin.activate_voting(request, queryset)

        mock_logger.error.assert_called_once()


@pytest.mark.django_db
class TestCloseVotingAction:
    def _make_admin(self):
        return EventVotingAdmin(EventVoting, admin.site)

    def _make_request(self):
        request = MagicMock()
        request._messages = MagicMock()
        return request

    def _make_event(self, event_id=1, description="Test Voting"):
        event = MagicMock(spec=EventVoting)
        event.id = event_id
        event.description = description
        return event

    def test_action_calls_service_with_event_id(self):
        event_admin = self._make_admin()
        request = self._make_request()
        event = self._make_event(event_id=20)
        queryset = [event]

        with patch("core.admin.voting.voting_service.close_vote") as mock_close:
            with patch.object(event_admin, "message_user"):
                event_admin.close_voting(request, queryset)

        mock_close.assert_called_once_with(20)

    def test_action_success_message_on_success(self):
        event_admin = self._make_admin()
        request = self._make_request()
        event = self._make_event(description="Eleição 2025")
        queryset = [event]

        with patch("core.admin.voting.voting_service.close_vote"):
            with patch.object(event_admin, "message_user") as mock_msg:
                event_admin.close_voting(request, queryset)

        mock_msg.assert_called_once_with(request, "Votação 'Eleição 2025' encerrada.")

    def test_action_error_message_on_service_exception(self):
        event_admin = self._make_admin()
        request = self._make_request()
        event = self._make_event()
        queryset = [event]

        with patch(
            "core.admin.voting.voting_service.close_vote",
            side_effect=Exception("erro ao encerrar"),
        ):
            with patch.object(event_admin, "message_user") as mock_msg:
                event_admin.close_voting(request, queryset)

        mock_msg.assert_called_once_with(request, "erro ao encerrar", level=ERROR)

    def test_action_logs_error_on_exception(self):
        event_admin = self._make_admin()
        request = self._make_request()
        event = self._make_event(event_id=9)
        queryset = [event]

        with patch("core.admin.voting.voting_service.close_vote", side_effect=Exception("fail")):
            with patch.object(event_admin, "message_user"):
                with patch("core.admin.voting.logger") as mock_logger:
                    event_admin.close_voting(request, queryset)

        mock_logger.error.assert_called_once()
