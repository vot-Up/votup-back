"""Custom S3 storage that generates proxy URLs instead of direct S3 URLs.

ImageField.url returns /media/<key> which routes through MediaProxyView.
The proxy generates a fresh presigned URL on each request, keeping the
bucket private while still serving files through Django.
"""

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class PrivateMediaStorage(S3Boto3Storage):
    """S3 storage that returns /media/<key> as the public URL.

    The actual S3 access happens via MediaProxyView, which generates
    short-lived presigned URLs on each request.
    """

    def url(self, name, parameters=None, expire=None, http_method=None):
        # Return the proxy URL instead of a direct S3 presigned URL
        return f"{settings.MEDIA_URL}{name}"
