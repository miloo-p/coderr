from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin view of the orders.
    """

    list_display = ["title", "customer_user", "business_user", "status", "created_at"]
