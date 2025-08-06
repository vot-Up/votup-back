from django.db.models import Subquery
from django_filters import filterset

from account import choices
from account import filters as account_filters
from core.models import models


class VoterFilter(account_filters.FilterBase):
    name = filterset.CharFilter(field_name="name", lookup_expr=choices.LIKE)
    cellphone = filterset.CharFilter(field_name="cellphone", lookup_expr=choices.EXACT)
    active = filterset.BooleanFilter(field_name="active", lookup_expr=choices.EXACT)

    class Meta:
        model = models.Voter
        fields = ["id", "created_at", "cellphone", "modified_at", "active", "name"]


class CandidateFilter(account_filters.FilterBase):
    name = filterset.CharFilter(field_name="name", lookup_expr=choices.LIKE)
    cellphone = filterset.CharFilter(field_name="cellphone", lookup_expr=choices.EXACT)
    exists = filterset.NumberFilter(method="exist")
    active = filterset.BooleanFilter(field_name="active", lookup_expr=choices.EXACT)
    plate_vice = filterset.CharFilter(method="get_plate_vice")
    plate_president = filterset.CharFilter(method="get_plate_president")
    user_plate = filterset.CharFilter(method="get_user_plate")

    @staticmethod
    def exist(queryset, name, value):
        subquery = models.PlateUser.objects.filter(plate__active=True).values("candidate_id")
        return queryset.exclude(id__in=Subquery(subquery))

    @staticmethod
    def get_user_plate(queryset, name, value):
        subquery = models.PlateUser.objects.all().values("candidate_id")
        return queryset.filter(id__in=Subquery(subquery))

    @staticmethod
    def get_plate_president(queryset, name, value):
        subquery = models.PlateUser.objects.filter(plate=value, type="P").values("candidate_id")
        return queryset.filter(id__in=Subquery(subquery))

    @staticmethod
    def get_plate_vice(queryset, name, value):
        subquery = models.PlateUser.objects.filter(plate=value, type="V").values("candidate_id")
        return queryset.filter(id__in=Subquery(subquery))

    class Meta:
        model = models.Candidate
        fields = ["id", "created_at", "cellphone", "modified_at", "active", "name", "exists"]


class PlateFilter(account_filters.FilterBase):
    name = filterset.CharFilter(field_name="name", lookup_expr=choices.LIKE)
    exists = filterset.NumberFilter(method="exist")
    active = filterset.BooleanFilter()
    voting = filterset.CharFilter(method="get_plate_voting")

    @staticmethod
    def exist(queryset, name, value):
        president = models.PlateUser.objects.filter(type="P").values("plate_id")
        president_and_vice = models.PlateUser.objects.filter(type="V", plate__in=Subquery(president)).values("plate_id")
        plates_not_filled = models.Plate.objects.all().exclude(id__in=Subquery(president_and_vice)).values("id")
        teste = queryset.exclude(id__in=Subquery(plates_not_filled))
        subquery = models.VotingPlate.objects.all().values("plate_id")
        return teste.exclude(id__in=Subquery(subquery))

    @staticmethod
    def get_plate_voting(queryset, name, value):
        subquery = models.VotingPlate.objects.filter(voting=value).values("plate_id")
        return queryset.filter(id__in=Subquery(subquery))

    class Meta:
        model = models.Plate
        fields = ["id", "created_at", "modified_at", "active", "name"]


class EventVotingFilter(account_filters.FilterBase):
    date = filterset.DateTimeFilter(field_name="date", lookup_expr=choices.EXACT)
    start_date = filterset.DateTimeFilter(field_name="date", lookup_expr=choices.GTE)
    final_date = filterset.DateTimeFilter(field_name="date", lookup_expr=choices.LTE)
    description = filterset.CharFilter(field_name="description", lookup_expr=choices.LIKE)
    plate_not_associate = filterset.NumberFilter(method="get_plate_not_associate")
    active = filterset.BooleanFilter(field_name="active", lookup_expr=choices.EXACT)

    @staticmethod
    def get_plate_not_associate(queryset, name, value):
        subquery = models.VotingPlate.objects.all().values("voting_id")
        plate_is_not_voting = models.Plate.objects.exclude(id__in=Subquery(subquery))
        return plate_is_not_voting

    class Meta:
        model = models.EventVoting
        fields = ["id", "created_at", "modified_at", "active", "date", "description"]


class PlateUserFilter(account_filters.FilterBase):
    candidate = filterset.CharFilter(field_name="candidate", lookup_expr=choices.EXACT)
    plate = filterset.CharFilter(field_name="plate", lookup_expr=choices.EXACT)
    type = filterset.CharFilter(field_name="type", lookup_expr=choices.IEXACT)

    class Meta:
        model = models.PlateUser
        fields = ["id", "created_at", "modified_at", "active", "candidate", "plate", "type"]


class VotingPlateFilter(account_filters.FilterBase):
    plate = filterset.CharFilter(field_name="plate", lookup_expr=choices.EXACT)
    voting = filterset.CharFilter(field_name="voting", lookup_expr=choices.EXACT)

    class Meta:
        model = models.VotingPlate
        fields = ["id", "created_at", "modified_at", "active", "plate", "voting"]


class VotingUserFilter(account_filters.FilterBase):
    voting = filterset.CharFilter(field_name="voting", lookup_expr=choices.EXACT)
    plate = filterset.CharFilter(field_name="plate", lookup_expr=choices.EXACT)
    voter = filterset.CharFilter(field_name="voter", lookup_expr=choices.EXACT)

    class Meta:
        model = models.VotingUser
        fields = ["id", "created_at", "modified_at", "active", "voting", "plate", "voter"]


class ResumeVoteFilter(account_filters.FilterBase):
    voting = filterset.CharFilter(field_name="voting", lookup_expr=choices.EXACT)
    plate = filterset.CharFilter(field_name="plate", lookup_expr=choices.EXACT)

    class Meta:
        model = models.ResumeVote
        fields = ["id", "created_at", "modified_at", "voting", "plate", "quantity"]
