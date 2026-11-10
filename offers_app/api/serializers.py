from rest_framework import serializers

from auth_app.models import CoderrUser

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


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    """
    Serializes the details key of an offer.
    """

    url = serializers.HyperlinkedIdentityField(view_name="offerdetail-infos")

    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "url",
        ]


class OfferUserDetailSerializer(serializers.ModelSerializer):
    """
    Serializes the user_details key of an offer.
    """

    class Meta:
        model = CoderrUser
        fields = [
            "first_name",
            "last_name",
            "username",
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

    def update(self, instance, validated_data):
        details = validated_data.pop("details", [])
        for detail in details:
            instance.details.filter(offer_type=detail["offer_type"]).update(**detail)
        return super().update(instance, validated_data)

    def validate_details(self, value):
        if not self.partial:
            offer_types = {detail["offer_type"] for detail in value}
            if len(value) != 3 or offer_types != {"basic", "standard", "premium"}:
                raise serializers.ValidationError(
                    "An offer needs details for all types: Basic, Standard and Premium."
                )
        else:
            for detail in value:
                if "offer_type" not in detail:
                    raise serializers.ValidationError("Each detail needs an offer_type.")

        return value


class OfferFilterSerializer(serializers.Serializer):
    """
    Serializes the query-filter inputs.
    """

    creator_id = serializers.IntegerField(required=False)
    max_delivery_time = serializers.IntegerField(required=False)
    min_price = serializers.FloatField(required=False)
    search = serializers.CharField(required=False)
    ordering = serializers.ChoiceField(
        choices=["min_price", "-min_price", "updated_at", "-updated_at"], required=False
    )


class OfferRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializes an offer.
    """

    details = OfferDetailLinkSerializer(many=True, read_only=True)
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
            "details",
            "min_price",
            "min_delivery_time",
        ]


class OfferListSerializer(OfferRetrieveSerializer):
    """
    Serializes an offer-list.
    """

    user_details = OfferUserDetailSerializer(read_only=True, source="user")

    class Meta(OfferRetrieveSerializer.Meta):
        fields = OfferRetrieveSerializer.Meta.fields + ["user_details"]
