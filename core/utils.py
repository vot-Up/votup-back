from account import serializers


def get_user(user, request=None):
    serializer = serializers.UserSerializer(user, context={"request": request})
    return serializer.data


def get_user_login(user, request=None):
    serializer = serializers.UserSerializer(user, context={"request": request})
    return serializer.data
