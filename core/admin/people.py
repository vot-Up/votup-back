import logging

from django.contrib import admin
from unfold.admin import ModelAdmin

from core.models.models import Candidate, Voter

logger = logging.getLogger(__name__)


@admin.register(Voter)
class VoterAdmin(ModelAdmin):
    list_display = ("name", "cellphone", "active", "created_at")
    search_fields = ("name", "cellphone")
    list_filter = ("active",)
    compressed_fields = True
    warn_unsaved_form = True


@admin.register(Candidate)
class CandidateAdmin(ModelAdmin):
    list_display = ("name", "cellphone", "disabled", "active", "created_at")
    search_fields = ("name", "cellphone")
    list_filter = ("disabled", "active")
    compressed_fields = True
    warn_unsaved_form = True
