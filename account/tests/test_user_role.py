import pytest
from django.core.exceptions import ValidationError


pytestmark = pytest.mark.django_db

USER_EXISTING_BLANK_FIELD_EXCLUDES = ["last_login", "avatar", "file_name"]


def test_user_role_allows_null(django_user_model):
    user = django_user_model.objects.create_user(
        email="null-role@test.com",
        password="testpass123",
        cellphone="11900000001",
        name="Null Role",
    )

    user.full_clean(exclude=USER_EXISTING_BLANK_FIELD_EXCLUDES)

    assert user.role is None


@pytest.mark.parametrize("role", ["ELEITOR", "CANDIDATO"])
def test_user_role_allows_supported_roles(django_user_model, role):
    user = django_user_model.objects.create_user(
        email=f"{role.lower()}@test.com",
        password="testpass123",
        cellphone=f"1190000000{1 if role == 'ELEITOR' else 2}",
        name=role.title(),
        role=role,
    )

    user.full_clean(exclude=USER_EXISTING_BLANK_FIELD_EXCLUDES)

    assert user.role == role


def test_user_role_rejects_invalid_value(django_user_model):
    user = django_user_model.objects.create_user(
        email="invalid-role@test.com",
        password="testpass123",
        cellphone="11900000003",
        name="Invalid Role",
        role="INVALID",
    )

    with pytest.raises(ValidationError) as exc_info:
        user.full_clean(exclude=USER_EXISTING_BLANK_FIELD_EXCLUDES)

    assert "role" in exc_info.value.message_dict


def test_superuser_keeps_null_role(django_user_model):
    user = django_user_model.objects.create_superuser(
        email="admin-role@test.com",
        password="testpass123",
        cellphone="11900000004",
        name="Admin Role",
    )

    user.full_clean(exclude=USER_EXISTING_BLANK_FIELD_EXCLUDES)

    assert user.is_staff is True
    assert user.role is None
