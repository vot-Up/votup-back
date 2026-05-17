import logging

from django.contrib import admin, messages
from unfold.admin import ModelAdmin, TabularInline

from core.models.models import EventVoting, ResumeVote, VotingPlate, VotingUser
from core.services import voting_service

logger = logging.getLogger(__name__)


class VotingPlateInline(TabularInline):
    model = VotingPlate
    tab = True


class VotingUserInline(TabularInline):
    model = VotingUser
    tab = True


class ResumeVoteInline(TabularInline):
    model = ResumeVote
    tab = True


@admin.register(EventVoting)
class EventVotingAdmin(ModelAdmin):
    list_display = ("description", "date", "active", "created_at")
    search_fields = ("description",)
    list_filter = ("active",)
    inlines = [VotingPlateInline, VotingUserInline, ResumeVoteInline]
    actions = ["activate_voting", "close_voting"]
    compressed_fields = True
    warn_unsaved_form = True

    def activate_voting(self, request, queryset):
        for event in queryset:
            try:
                voting_service.active_vote(event.id)
                self.message_user(request, f"Votação '{event.description}' ativada.")
            except Exception as e:
                logger.error("Erro ao ativar votação %s: %s", event.id, e)
                self.message_user(request, str(e), level=messages.ERROR)

    activate_voting.short_description = "Ativar votação selecionada"

    def close_voting(self, request, queryset):
        for event in queryset:
            try:
                voting_service.close_vote(event.id)
                self.message_user(request, f"Votação '{event.description}' encerrada.")
            except Exception as e:
                logger.error("Erro ao encerrar votação %s: %s", event.id, e)
                self.message_user(request, str(e), level=messages.ERROR)

    close_voting.short_description = "Encerrar votação selecionada"


@admin.register(VotingPlate)
class VotingPlateAdmin(ModelAdmin):
    list_display = ("voting", "plate", "active", "created_at")
    search_fields = ("voting__description", "plate__name")
    list_filter = ("active",)
    compressed_fields = True
    warn_unsaved_form = True


@admin.register(VotingUser)
class VotingUserAdmin(ModelAdmin):
    list_display = ("voting", "voter", "plate", "active", "created_at")
    search_fields = ("voting__description", "voter__name", "plate__name")
    list_filter = ("active",)
    compressed_fields = True
    warn_unsaved_form = True


@admin.register(ResumeVote)
class ResumeVoteAdmin(ModelAdmin):
    list_display = ("voting", "plate", "quantity", "active", "created_at")
    search_fields = ("voting__description", "plate__name")
    list_filter = ("active",)
    compressed_fields = True
    warn_unsaved_form = True
