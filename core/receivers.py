from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from account import models as core_models

from core import models


@receiver(post_save, sender=models.EventVoting, dispatch_uid="deactivate_other_votings")
def deactivate_other_votings(sender, instance, created, **kwargs):
    if created:
        models.EventVoting.objects.filter(active=True).exclude(pk=instance.pk).update(active=False)


@receiver(post_delete, sender=core_models.User)
def delete_image(sender, instance, **kwargs):
    if instance.avatar:
        image_path = instance.avatar.name
        default_storage.delete(image_path)


@receiver(post_delete, sender=models.Candidate)
def delete_image_candidate(sender, instance, **kwargs):
    if instance.avatar:
        image_path = instance.avatar.name
        default_storage.delete(image_path)


@receiver(post_delete, sender=models.Voter)
def delete_image_voter(sender, instance, **kwargs):
    if instance.avatar:
        image_path = instance.avatar.name
        default_storage.delete(image_path)
