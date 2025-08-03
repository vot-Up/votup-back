from rest_framework import serializers

from account import serializers as account_serializers
from core.models import models


class VoterSerializer(account_serializers.SerializerBase):
    class Meta:
        model = models.Voter
        fields = '__all__'


class CandidateSerializer(account_serializers.SerializerBase):
    class Meta:
        model = models.Candidate
        fields = '__all__'


class PlateSerializer(account_serializers.SerializerBase):
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


class EventVotingSerializer(account_serializers.SerializerBase):
    was_voted = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.EventVoting
        fields = '__all__'


class PlateUserSerializer(account_serializers.SerializerBase):
    class Meta:
        model = models.PlateUser
        fields = '__all__'

    expandable_fields = {
        'candidate': (
            'core.CandidateSerializer',
            {'fields': ['id', 'name']}
        ),
    }


class PlateUserPresidentsOrViceSerializer(account_serializers.SerializerBase):
    candidate = CandidateSerializer()
    plate = PlateSerializer()

    class Meta:
        model = models.PlateUser
        fields = '__all__'


class VotingPlateSerializer(account_serializers.SerializerBase):
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


class VotingUserSerializer(account_serializers.SerializerBase):
    class Meta:
        model = models.VotingUser
        fields = '__all__'


class ResumeVoteSerializer(account_serializers.SerializerBase):
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
