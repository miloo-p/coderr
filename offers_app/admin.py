from django.contrib import admin

from .models import Offer, OfferDetail


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """
    Admin view of the offers.
    """

    list_display = ["title", "user", "updated_at"]


@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    """
    Admin view of the offer packages.
    """

    list_display = ["title", "offer", "offer_type", "price"]
