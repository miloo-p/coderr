from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CoderrUser


@admin.register(CoderrUser)
class CoderrUserAdmin(UserAdmin):
    """
    Admin view of the user with the extra profile fields.
    """

    fieldsets = UserAdmin.fieldsets + (
        (("Profile Picture"), {"fields": ("file",)}),
        (("More Info"), {"fields": ("location", "tel", "description", "working_hours")}),
        (("Profile Type"), {"fields": ("type",)}),
    )
