from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin view of the reviews.
    """

    list_display = ["business_user", "reviewer", "rating", "updated_at"]
