from django.contrib import admin

from .models import Offer, OfferDetail


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    pass


@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    pass
