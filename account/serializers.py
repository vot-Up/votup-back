from django.contrib.auth.hashers import make_password
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account import models
from core import utils


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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["user_id"] = user.id
        token["username"] = user.username
        token["email"] = user.email
        token["user"] = utils.get_user(user)

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return {"token": data, "user": utils.get_user_login(self.user)}
