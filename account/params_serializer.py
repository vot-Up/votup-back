from rest_framework import serializers


class PlateUserParamSerializer(serializers.Serializer):
    candidate = serializers.IntegerField(required=True)
    plate = serializers.IntegerField(required=True)


class VotingPlateParamSerializer(serializers.Serializer):
    plate = serializers.IntegerField(required=True)
    voting = serializers.IntegerField(required=True)


class VoterPlateParamsSerializer(serializers.Serializer):
    plate = serializers.IntegerField(required=False)


class VotingUserParamsSerializer(serializers.Serializer):
    event_vote = serializers.IntegerField(required=False)


class ResumeVoteParamsSerializer(serializers.Serializer):
    event_vote = serializers.IntegerField(required=False)


class InitVotingParamSerializer(serializers.Serializer):
    cellphone = serializers.CharField(required=True)


class ActiveOrCloseVoteParamSerializer(serializers.Serializer):
    vote_id = serializers.IntegerField(required=True)


class UserSerializerParams(serializers.Serializer):
    avatar = serializers.ListField(
        child=serializers.FileField(),
        required=False,
        allow_null=True
    )


class ResetPasswordSerializerParams(serializers.Serializer):
    cellphone = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    new_password = serializers.CharField(required=True)


class EventVotingSerializerParams(serializers.Serializer):
    plate = cellphone = serializers.IntegerField(required=True)
    voting = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)


class ResumeVotingSerializerParams(serializers.Serializer):
    event_vote = serializers.IntegerField(required=True)


class VoterInPlateSerializerParams(serializers.Serializer):
    event_vote = serializers.IntegerField(required=True)
    plate = serializers.IntegerField(required=True)
