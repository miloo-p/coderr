from rest_framework import serializers

from ..models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializes the OfferDetails.
    """

    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]


class OfferSerializer(serializers.ModelSerializer):
    """
    Serializes the Offer with its three OfferDetails.
    """

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "title",
            "image",
            "description",
            "details",
        ]

    def create(self, validated_data):
        details = validated_data.pop("details")
        offer = Offer.objects.create(**validated_data)
        for detail in details:
            OfferDetail.objects.create(offer=offer, **detail)

        return offer

    def validate_details(self, value):
        offer_types = {detail["offer_type"] for detail in value}
        if len(value) != 3 or offer_types != {"basic", "standard", "premium"}:
            raise serializers.ValidationError(
                "An offer needs details for all types: Basic, Standard and Premium."
            )
        return value


class OfferRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializes the OfferDetails.
    """

    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "min_price",
            "min_delivery_time",
        ]
