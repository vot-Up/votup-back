"""Views para servir arquivos de mídia do S3 via presigned URL."""

import logging

import boto3
from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views import View

logger = logging.getLogger(__name__)


class MediaProxyView(View):
    """Serve arquivos do S3 sem expor o bucket.

    Tenta fazer stream direto do S3. Se o conteúdo for grande,
    gera uma presigned URL e redireciona. O bucket permanece
    privado — apenas URLs assinadas concedem acesso temporário.

    URL format: /media/<path>
    Exemplo: /media/20260517034811.jpeg
    """

    def get(self, request, path):
        client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        )

        try:
            response = client.get_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=path,
            )
        except client.exceptions.NoSuchKey:
            raise Http404(f"Arquivo não encontrado: {path}")
        except client.exceptions.ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "")
            if error_code == "404":
                raise Http404(f"Arquivo não encontrado: {path}")
            logger.error("Erro S3 ao buscar %s: %s", path, e)
            raise Http404("Erro ao buscar arquivo.")

        content_type = response.get("ContentType", "application/octet-stream")
        content_length = response.get("ContentLength", 0)
        body = response["Body"].read()

        return HttpResponse(
            body,
            content_type=content_type,
            headers={
                "Content-Length": str(content_length),
                "Cache-Control": "private, max-age=3600",
            },
        )
