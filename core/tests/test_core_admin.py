"""Unit tests for core/admin module (Task 03)."""

from unittest.mock import MagicMock, patch

import pytest
from django.contrib import admin
from django.contrib.messages import ERROR

from core.admin.people import CandidateAdmin, VoterAdmin
from core.admin.plates import PlateAdmin, PlateUserAdmin, PlateUserInline
from core.models.models import Candidate, Plate, PlateUser, Voter


class TestAdminRegistrations:
    def test_voter_admin_registered(self):
        assert isinstance(admin.site._registry.get(Voter), VoterAdmin)

    def test_candidate_admin_registered(self):
        assert isinstance(admin.site._registry.get(Candidate), CandidateAdmin)

    def test_plate_admin_registered(self):
        assert isinstance(admin.site._registry.get(Plate), PlateAdmin)

    def test_plate_user_admin_registered(self):
        assert isinstance(admin.site._registry.get(PlateUser), PlateUserAdmin)


class TestPlateAdminInlines:
    def test_plate_user_inline_in_plate_admin(self):
        assert PlateUserInline in PlateAdmin.inlines


class TestUnfoldAdminConfig:
    @pytest.mark.parametrize("admin_cls", [VoterAdmin, CandidateAdmin, PlateAdmin, PlateUserAdmin])
    def test_compressed_fields(self, admin_cls):
        assert admin_cls.compressed_fields is True

    @pytest.mark.parametrize("admin_cls", [VoterAdmin, CandidateAdmin, PlateAdmin, PlateUserAdmin])
    def test_warn_unsaved_form(self, admin_cls):
        assert admin_cls.warn_unsaved_form is True


class TestVoterAdminConfig:
    def test_list_display(self):
        assert VoterAdmin.list_display == ("name", "cellphone", "active", "created_at")

    def test_search_fields(self):
        assert VoterAdmin.search_fields == ("name", "cellphone")

    def test_list_filter(self):
        assert VoterAdmin.list_filter == ("active",)


class TestCandidateAdminConfig:
    def test_list_display(self):
        assert CandidateAdmin.list_display == ("name", "cellphone", "disabled", "active", "created_at")

    def test_search_fields(self):
        assert CandidateAdmin.search_fields == ("name", "cellphone")

    def test_list_filter(self):
        assert CandidateAdmin.list_filter == ("disabled", "active")


class TestPlateAdminConfig:
    def test_list_display(self):
        assert PlateAdmin.list_display == ("name", "active", "created_at")

    def test_search_fields(self):
        assert PlateAdmin.search_fields == ("name",)

    def test_list_filter(self):
        assert PlateAdmin.list_filter == ("active",)


class TestPlateUserAdminConfig:
    def test_list_display(self):
        assert PlateUserAdmin.list_display == ("plate", "candidate", "type", "active")

    def test_search_fields(self):
        assert PlateUserAdmin.search_fields == ("plate__name", "candidate__name")

    def test_list_filter(self):
        assert PlateUserAdmin.list_filter == ("type", "active")


@pytest.mark.django_db
class TestActivatePlateAction:
    def _make_plate_admin(self):
        return PlateAdmin(Plate, admin.site)

    def _make_request(self):
        request = MagicMock()
        request._messages = MagicMock()
        return request

    def _make_plate(self, plate_id=1, name="Test Plate"):
        plate = MagicMock(spec=Plate)
        plate.id = plate_id
        plate.name = name
        return plate

    def test_action_calls_service_with_plate_id(self):
        plate_admin = self._make_plate_admin()
        request = self._make_request()
        plate = self._make_plate(plate_id=42)
        queryset = [plate]

        with patch("core.admin.plates.plate_service.activate_plate") as mock_activate:
            with patch.object(plate_admin, "message_user"):
                plate_admin.activate_plate_action(request, queryset)

        mock_activate.assert_called_once_with(42)

    def test_action_success_message_on_success(self):
        plate_admin = self._make_plate_admin()
        request = self._make_request()
        plate = self._make_plate(name="Chapa Alpha")
        queryset = [plate]

        with patch("core.admin.plates.plate_service.activate_plate"):
            with patch.object(plate_admin, "message_user") as mock_msg:
                plate_admin.activate_plate_action(request, queryset)

        mock_msg.assert_called_once_with(request, "Chapa 'Chapa Alpha' ativada com sucesso.")

    def test_action_error_message_on_service_exception(self):
        plate_admin = self._make_plate_admin()
        request = self._make_request()
        plate = self._make_plate()
        queryset = [plate]

        with patch("core.admin.plates.plate_service.activate_plate", side_effect=Exception("business rule violated")):
            with patch.object(plate_admin, "message_user") as mock_msg:
                plate_admin.activate_plate_action(request, queryset)

        mock_msg.assert_called_once_with(request, "business rule violated", level=ERROR)

    def test_action_logs_error_on_exception(self):
        plate_admin = self._make_plate_admin()
        request = self._make_request()
        plate = self._make_plate(plate_id=7)
        queryset = [plate]

        with patch("core.admin.plates.plate_service.activate_plate", side_effect=Exception("fail")):
            with patch.object(plate_admin, "message_user"):
                with patch("core.admin.plates.logger") as mock_logger:
                    plate_admin.activate_plate_action(request, queryset)

        mock_logger.error.assert_called_once()
