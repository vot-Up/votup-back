from botocore.exceptions import ClientError
from django.core.files.base import ContentFile
from django.db import transaction

from account import exceptions, models


class UserActions:
    @staticmethod
    @transaction.atomic
    def create_avatar(**kwargs):
        try:
            for item in kwargs.get("avatar"):
                avatar = models.User()
                avatar.avatar = ContentFile(name=item.name, content=item.read())
                avatar.file_name = item.name
                avatar.save()
        except ClientError:
            raise exceptions.MinioException()

    @staticmethod
    def reset_password(new_password: str, cellphone: str, email: str):
        try:
            valid_user = models.User.objects.get(cellphone=cellphone, email=email)
        except Exception:
            raise exceptions.UserNotExistException

        if new_password:
            valid_user.set_password(raw_password=new_password)
            valid_user.save()
