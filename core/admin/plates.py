import logging

from django.contrib import admin, messages
from unfold.admin import ModelAdmin, TabularInline

from core.models.models import Plate, PlateUser
from core.services import plate_service

logger = logging.getLogger(__name__)


class PlateUserInline(TabularInline):
    model = PlateUser
    tab = True


@admin.register(Plate)
class PlateAdmin(ModelAdmin):
    list_display = ("name", "active", "created_at")
    search_fields = ("name",)
    list_filter = ("active",)
    inlines = [PlateUserInline]
    actions = ["activate_plate_action"]
    compressed_fields = True
    warn_unsaved_form = True

    def activate_plate_action(self, request, queryset):
        for plate in queryset:
            try:
                plate_service.activate_plate(plate.id)
                self.message_user(request, f"Chapa '{plate.name}' ativada com sucesso.")
            except Exception as e:
                logger.error("Erro ao ativar chapa %s: %s", plate.id, e)
                self.message_user(request, str(e), level=messages.ERROR)

    activate_plate_action.short_description = "Ativar chapa selecionada"


@admin.register(PlateUser)
class PlateUserAdmin(ModelAdmin):
    list_display = ("plate", "candidate", "type", "active")
    search_fields = ("plate__name", "candidate__name")
    list_filter = ("type", "active")
    compressed_fields = True
    warn_unsaved_form = True
