from django.shortcuts import get_object_or_404
from rest_framework import serializers

from offers_app.models import OfferDetail

from ..models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializes an order.
    """

    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        read_only_fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]
        fields = [
            "offer_detail_id",
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        offer_detail_id = validated_data.pop("offer_detail_id")
        offer_detail = get_object_or_404(OfferDetail, pk=offer_detail_id)
        order = Order.objects.create(
            **validated_data,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            business_user=offer_detail.offer.user,
        )
        return order
