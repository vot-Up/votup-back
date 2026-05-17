import boto3
from django.conf import settings


class S3FileStorageAdapter:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        )
        self.bucket = settings.AWS_STORAGE_BUCKET_NAME

    def upload(self, file: bytes, filename: str) -> str:
        self.client.put_object(Bucket=self.bucket, Key=filename, Body=file)
        return f"{settings.AWS_S3_ENDPOINT_URL}/{self.bucket}/{filename}"

    def delete(self, file_url: str) -> None:
        key = file_url.split("/")[-1]
        self.client.delete_object(Bucket=self.bucket, Key=key)
