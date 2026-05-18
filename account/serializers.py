from django.contrib.auth.hashers import make_password
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account import messages as account_messages
from account import models
from core import utils
from core.models import models as core_models


class SerializerBase(FlexFieldsModelSerializer, serializers.HyperlinkedModelSerializer):
    def get_field_names(self, declared_fields, info):
        fields = super().get_field_names(declared_fields, info)
        fields.insert(0, "id")
        return fields


class UserSerializer(SerializerBase):
    def validate_password(self, value: str) -> str:
        """Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)

    class Meta:
        model = models.User
        fields = "__all__"


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=256)
    email = serializers.EmailField()
    cellphone = serializers.CharField(max_length=64)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=["ELEITOR", "CANDIDATO"])

    def validate_email(self, value):
        if models.User.objects.filter(email=value).exists():
            raise serializers.ValidationError(account_messages.EMAIL_ALREADY_EXISTS)
        return value

    def validate_cellphone(self, value):
        if (
            models.User.objects.filter(cellphone=value).exists()
            or core_models.Voter.objects.filter(cellphone=value).exists()
            or core_models.Candidate.objects.filter(cellphone=value).exists()
        ):
            raise serializers.ValidationError(account_messages.CELLPHONE_ALREADY_EXISTS)
        return value

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Senhas não conferem."})
        return data

    def create(self, validated_data):
        role = validated_data["role"]
        user = models.User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            cellphone=validated_data["cellphone"],
            name=validated_data["name"],
            role=role,
        )
        profile_data = {
            "name": validated_data["name"],
            "cellphone": validated_data["cellphone"],
            "user": user,
        }
        if role == "ELEITOR":
            core_models.Voter.objects.create(**profile_data)
        else:
            core_models.Candidate.objects.create(**profile_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["user_id"] = user.id
        token["username"] = user.username
        token["email"] = user.email
        token["role"] = user.role
        token["user"] = utils.get_user(user)

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return {"token": data, "user": utils.get_user_login(self.user)}
