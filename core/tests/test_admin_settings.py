"""Unit tests for Unfold admin settings configuration (Task 01)."""

import pytest
from django.conf import settings


@pytest.mark.django_db
class TestUnfoldSettings:
    """Verify UNFOLD dict and INSTALLED_APPS configuration."""

    def test_unfold_dict_exists(self):
        """UNFOLD settings dict exists and contains required keys."""
        assert hasattr(settings, "UNFOLD")
        unfold = settings.UNFOLD
        assert "SITE_TITLE" in unfold
        assert "SITE_HEADER" in unfold
        assert "SITE_SYMBOL" in unfold
        assert "SHOW_HISTORY" in unfold
        assert "SIDEBAR" in unfold

    def test_sidebar_has_four_sections(self):
        """SIDEBAR navigation has exactly 4 sections with correct titles."""
        navigation = settings.UNFOLD["SIDEBAR"]["navigation"]
        assert len(navigation) == 4
        titles = [section["title"] for section in navigation]
        assert "Votação" in titles
        assert "Pessoas" in titles
        assert "Chapas" in titles
        assert "Sistema" in titles

    def test_unfold_before_django_admin_in_installed_apps(self):
        """"unfold" appears in INSTALLED_APPS before "django.contrib.admin"."""
        apps = settings.INSTALLED_APPS
        unfold_idx = apps.index("unfold")
        admin_idx = apps.index("django.contrib.admin")
        assert unfold_idx < admin_idx

    def test_simple_history_in_installed_apps(self):
        """"simple_history" appears in INSTALLED_APPS."""
        assert "simple_history" in settings.INSTALLED_APPS

    def test_unfold_contrib_in_installed_apps(self):
        """"unfold.contrib.filters" and "unfold.contrib.simple_history" in INSTALLED_APPS."""
        assert "unfold.contrib.filters" in settings.INSTALLED_APPS
        assert "unfold.contrib.simple_history" in settings.INSTALLED_APPS

    def test_reversion_not_in_installed_apps(self):
        """"reversion" does NOT appear in INSTALLED_APPS."""
        assert "reversion" not in settings.INSTALLED_APPS

    def test_show_history_enabled(self):
        """SHOW_HISTORY is True in UNFOLD settings."""
        assert settings.UNFOLD["SHOW_HISTORY"] is True

    def test_sidebar_search_enabled(self):
        """Sidebar search and command_search are enabled."""
        assert settings.UNFOLD["SIDEBAR"]["show_search"] is True
        assert settings.UNFOLD["SIDEBAR"]["command_search"] is True

    def test_sidebar_sections_are_collapsible(self):
        """All sidebar sections have collapsible=True."""
        for section in settings.UNFOLD["SIDEBAR"]["navigation"]:
            assert section["collapsible"] is True

    def test_sidebar_items_have_links(self):
        """All sidebar items have title, icon, and link fields."""
        for section in settings.UNFOLD["SIDEBAR"]["navigation"]:
            for item in section["items"]:
                assert "title" in item
                assert "icon" in item
                assert "link" in item

    def test_history_request_middleware_in_middleware(self):
        """HistoryRequestMiddleware is in MIDDLEWARE for simple-history user tracking."""
        assert "simple_history.middleware.HistoryRequestMiddleware" in settings.MIDDLEWARE
