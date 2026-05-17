from rest_framework.exceptions import APIException

from core import messages


class ActionFailedException(APIException):
    default_detail = messages.ACTION_FAILED

    def __init__(self, cause: str, status_code=500):
        self.status_code = status_code
        super().__init__(detail=self.default_detail % (cause,))


class PermissionNotAllowedException(APIException):
    status_code = 400
    default_detail = messages.PERMISSION_NOT_ALLOWED


class UserNotExistException(APIException):
    status = 400
    default_detail = messages.USER_INVALID


class MinioException(APIException):
    status_code = 400
    default_detail = messages.MINIO_FAILURE


class InvalidCredentialsException(APIException):
    status_code = 405
    default_detail = messages.INVALID_CREDENTIALS


class PlateUserIsActiveException(APIException):
    pass
