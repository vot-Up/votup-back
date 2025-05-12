from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core import models, utils
from rest_flex_fields import FlexFieldsModelSerializer


class SerializerBase(FlexFieldsModelSerializer, serializers.HyperlinkedModelSerializer):

    def get_field_names(self, declared_fields, info):
        fields = super().get_field_names(declared_fields, info)
        fields.insert(0, 'id')
        return fields


class UserSerializer(SerializerBase):
    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)

    class Meta:
        model = models.User
        fields = '__all__'


class VoterSerializer(SerializerBase):
    class Meta:
        model = models.Voter
        fields = '__all__'


class CandidateSerializer(SerializerBase):
    class Meta:
        model = models.Candidate
        fields = '__all__'


class PlateSerializer(SerializerBase):
    was_voted = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Plate
        fields = '__all__'

    expandable_fields = {
        'plate': (
            'core.PlateUserPresidentsOrViceSerializer',
            {'fields': ['id', 'candidate', 'type'], "many": True}
        ),
    }


class EventVotingSerializer(SerializerBase):
    was_voted = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.EventVoting
        fields = '__all__'


class PlateUserSerializer(SerializerBase):
    class Meta:
        model = models.PlateUser
        fields = '__all__'

    expandable_fields = {
        'candidate': (
            'core.CandidateSerializer',
            {'fields': ['id', 'name']}
        ),
    }


class PlateUserPresidentsOrViceSerializer(SerializerBase):
    candidate = CandidateSerializer()
    plate = PlateSerializer()

    class Meta:
        model = models.PlateUser
        fields = '__all__'


class VotingPlateSerializer(SerializerBase):
    class Meta:
        model = models.VotingPlate
        fields = '__all__'

    expandable_fields = {
        'plate': (
            'core.PlateSerializer',
            {'fields': ['id', 'url', 'name', 'active', 'was_voted']}
        ),
        'voting': (
            'core.EventVotingSerializer',
            {'fields': ['id', 'url', 'description', 'date']}
        )
    }


class VotingUserSerializer(SerializerBase):
    class Meta:
        model = models.VotingUser
        fields = '__all__'


class ResumeVoteSerializer(SerializerBase):
    class Meta:
        model = models.ResumeVote
        fields = '__all__'

    expandable_fields = {
        'plate': (
            'core.PlateSerializer',
            {'fields': ['id', 'name']}
        ),
        'voting': (
            'core.EventVotingSerializer',
            {'fields': ['id', 'description']}
        )
    }


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        token['user'] = utils.get_user(user)

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return {
            'token': data,
            'user': utils.get_user_login(self.user)
        }
