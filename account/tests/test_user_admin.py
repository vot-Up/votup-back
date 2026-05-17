"""Unit and integration tests for account/admin.py (Task 05)."""

import pytest
from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from account.admin import UserAdmin
from account.models import User


class TestUserAdminRegistration:
    def test_user_admin_registered(self):
        assert isinstance(admin.site._registry.get(User), UserAdmin)

    def test_group_auto_registered(self):
        assert Group in admin.site._registry

    def test_token_proxy_auto_registered(self):
        assert TokenProxy in admin.site._registry


class TestUserAdminUnfoldConfig:
    def test_compressed_fields(self):
        assert UserAdmin.compressed_fields is True

    def test_warn_unsaved_form(self):
        assert UserAdmin.warn_unsaved_form is True


class TestUserAdminListConfig:
    def test_list_display(self):
        assert UserAdmin.list_display == ("avatar_thumbnail", "email", "name", "cellphone", "is_staff", "is_active", "created_at")

    def test_search_fields(self):
        assert UserAdmin.search_fields == ("email", "name", "cellphone")

    def test_list_filter(self):
        assert UserAdmin.list_filter == ("is_staff", "is_active")


@pytest.mark.django_db
class TestUserAdminUrls:
    @pytest.fixture
    def superuser(self, django_user_model):
        return django_user_model.objects.create_superuser(
            email="admin@test.com",
            password="adminpass",
            name="Admin",
            cellphone="11999999999",
        )

    @pytest.fixture
    def admin_client(self, client, superuser):
        client.force_login(superuser)
        return client

    def test_user_changelist_url_loads(self, admin_client):
        response = admin_client.get("/admin/account/user/")
        assert response.status_code == 200

    def test_group_changelist_url_loads(self, admin_client):
        response = admin_client.get("/admin/auth/group/")
        assert response.status_code == 200

    def test_token_proxy_changelist_url_loads(self, admin_client):
        response = admin_client.get("/admin/authtoken/tokenproxy/")
        assert response.status_code == 200
