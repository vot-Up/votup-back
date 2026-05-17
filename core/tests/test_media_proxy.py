"""Tests for PrivateMediaStorage and MediaProxyView."""

import pytest
from django.conf import settings
from django.test import Client

from core.storage import PrivateMediaStorage


class TestPrivateMediaStorage:
    """Verify PrivateMediaStorage generates proxy URLs instead of direct S3 URLs."""

    def test_url_returns_media_proxy_path(self):
        storage = PrivateMediaStorage()
        url = storage.url("20260517034811.jpeg")
        assert url == "/media/20260517034811.jpeg"

    def test_url_does_not_contain_s3_endpoint(self):
        storage = PrivateMediaStorage()
        url = storage.url("20260517034811.jpeg")
        assert "localhost:9000" not in url
        assert "amazonaws.com" not in url

    def test_url_does_not_contain_signature(self):
        storage = PrivateMediaStorage()
        url = storage.url("20260517034811.jpeg")
        assert "AWSAccessKeyId" not in url
        assert "Signature" not in url

    def test_url_prefixed_with_media_url(self):
        storage = PrivateMediaStorage()
        url = storage.url("somefile.png")
        assert url.startswith(settings.MEDIA_URL)


@pytest.mark.django_db
class TestMediaProxyView:
    """Verify MediaProxyView serves S3 files via Django."""

    def test_proxy_returns_image(self):
        """Existing S3 file is served with 200 and correct content type."""
        # Requires a file in S3 — uses the existing test upload
        from core.models.models import Voter
        from django.core.files.base import ContentFile

        voter = Voter.objects.create(name="Proxy Test", cellphone="11900000001")
        voter.avatar.save("proxy_test.png", ContentFile(b"\x89PNG\r\ntest"), save=True)
        key = voter.avatar.name

        client = Client()
        resp = client.get(f"/media/{key}")
        assert resp.status_code == 200
        assert resp["Content-Type"] in ("image/png", "application/octet-stream")
        assert len(resp.content) > 0

        # Cleanup
        voter.avatar.delete(save=False)
        voter.delete()

    def test_proxy_404_for_missing_file(self):
        """Non-existent S3 file returns 404."""
        client = Client()
        resp = client.get("/media/nonexistent_file_12345.png")
        assert resp.status_code == 404

    def test_proxy_has_cache_header(self):
        """Response includes Cache-Control for browser caching."""
        from core.models.models import Voter
        from django.core.files.base import ContentFile

        voter = Voter.objects.create(name="Cache Test", cellphone="11900000002")
        voter.avatar.save("cache_test.png", ContentFile(b"\x89PNG\r\ntest"), save=True)
        key = voter.avatar.name

        client = Client()
        resp = client.get(f"/media/{key}")
        assert "Cache-Control" in resp
        assert "max-age=3600" in resp["Cache-Control"]

        # Cleanup
        voter.avatar.delete(save=False)
        voter.delete()
