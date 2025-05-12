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


class ForeignKeyException(APIException):
    status_code = 400
    default_detail = messages.FOREIGN_KEY_EXCEPTION


class InvalidPasswordException(APIException):
    status_code = 405
    default_detail = messages.INVALID_PASSWORD


class SettingsEmailNotFoundException(APIException):
    status_code = 500
    default_detail = messages.SETTINGS_EMAIL_NOT_FOUND


class InvalidSecretKeyException(APIException):
    status_code = 500
    default_detail = messages.INVALID_SECRET_KEY


class ErrorToSendEmailException(APIException):
    status_code = 500
    default_detail = messages.ERROR_TO_SEND_EMAIL


class ReportServerUnavailableException(APIException):
    status_code = 500
    default_detail = messages.REPORT_SERVER_UNAVAILABLE


class UserNotFoundException(APIException):
    status_code = 500
    default_detail = messages.USER_NOT_FOUND


class NoRecordFoundException(APIException):
    status_code = 500
    default_detail = messages.NO_RECORD_FOUND


class MinioException(APIException):
    status_code = 400
    default_detail = messages.MINIO_FAILURE


class GroupDoesNotExistsException(APIException):
    status_code = 400
    default_detail = messages.GROUP_DOES_NOT_EXISTS


class NoActiveVotingException(APIException):
    status_code = 400
    default_detail = messages.NO_ACTIVE_VOTING


class UserHasAlreadyVotedException(APIException):
    status_code = 400
    default_detail = messages.USER_HAS_ALREADY_VOTED


class candidateAssociateException(APIException):
    status_code = 400
    default_detail = "candidate associate"


class EventVotingException(APIException):
    status_code = 400
    default_detail = messages.EVENT_VOTING_ERROR


class TimeOverVotingException(APIException):
    status_code = 400
    default_detail = messages.TIME_OVER_VOTING


class InvalidCredentialsException(APIException):
    status_code = 405
    default_detail = messages.INVALID_CREDENTIALS


class DeleteVoteActiveException(APIException):
    status_code = 400
    default_detail = messages.INVALID_DELETE_VOTE


class ExistVoteActiveException(APIException):
    status = 400
    default_detail = messages.EXISTS_VOTE_ACTIVE


class UserNotExistException(APIException):
    status = 400
    default_detail = messages.USER_INVALID


class UnableRemoveUserException(APIException):
    status = 400
    default_detail = messages.UNABLE_REMOVE_USER


class UnableRemovePlateException(APIException):
    status = 400
    default_detail = messages.UNABLE_REMOVE_PLATE


class CellphoneDoesNotUserException(APIException):
    status = 400
    default_detail = messages.CELLPHONE_DOES_NOT_USER


class PlateUserIsActiveException(APIException):
    status = 400
    default_detail = messages.PLATE_USER_ACTIVE
