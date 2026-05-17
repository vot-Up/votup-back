import logging

from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display

from core.models.models import Candidate, Voter

logger = logging.getLogger(__name__)


@admin.register(Voter)
class VoterAdmin(ModelAdmin):
    list_display = ("name", "cellphone", "avatar_thumbnail", "active", "created_at")
    search_fields = ("name", "cellphone")
    list_filter = ("active",)
    compressed_fields = True
    warn_unsaved_form = True

    @display(description="Avatar", image=True)
    def avatar_thumbnail(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None


@admin.register(Candidate)
class CandidateAdmin(ModelAdmin):
    list_display = ("name", "cellphone", "avatar_thumbnail", "disabled", "active", "created_at")
    search_fields = ("name", "cellphone")
    list_filter = ("disabled", "active")
    compressed_fields = True
    warn_unsaved_form = True

    @display(description="Avatar", image=True)
    def avatar_thumbnail(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None
