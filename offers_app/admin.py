from django.contrib import admin

from .models import Offer, OfferDetail


@admin.register(Offer)
class BoardAdmin(admin.ModelAdmin):
    pass


@admin.register(OfferDetail)
class TaskAdmin(admin.ModelAdmin):
    pass
