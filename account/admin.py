from django.contrib import admin
from unfold.admin import ModelAdmin

from account.models import User


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ("email", "name", "cellphone", "is_staff", "is_active", "created_at")
    search_fields = ("email", "name", "cellphone")
    list_filter = ("is_staff", "is_active")
    compressed_fields = True
    warn_unsaved_form = True
