from django.db import models
from django.db.models import Count


class VotingUserManager(models.Manager):
    def ranking(self, voting_id: int):
        return self.get_queryset().values('plate__id', 'plate__name').annotate(
            total=Count('*')
        ).filter(voting_id=voting_id, voter__isnull=False, ).order_by('-total')
