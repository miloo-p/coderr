from rest_framework import serializers

from ..models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializes a review.
    """

    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "reviewer", "created_at", "updated_at"]

    def validate_business_user(self, value):
        """
        Allows reviews only for business users.
        """
        if value.type != "business":
            raise serializers.ValidationError("Reviews can only be written for business users.")
        return value

    def validate(self, attrs):
        """
        Allows only one review per customer and business user.
        """
        if self.instance is None:
            reviewer = self.context["request"].user
            if Review.objects.filter(
                business_user=attrs["business_user"], reviewer=reviewer
            ).exists():
                raise serializers.ValidationError("You have already reviewed this business user.")
        return attrs


class ReviewFilterSerializer(serializers.Serializer):
    """
    Serializes the query-filter inputs of the review list.
    """

    business_user_id = serializers.IntegerField(required=False)
    reviewer_id = serializers.IntegerField(required=False)
    ordering = serializers.ChoiceField(
        choices=["updated_at", "-updated_at", "rating", "-rating"], required=False
    )


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """
    Serializes the editable fields of a review.
    """

    class Meta:
        model = Review
        fields = ["rating", "description"]

    def validate(self, attrs):
        """
        Rejects every field except rating and description.
        """
        extra_fields = set(self.initial_data) - {"rating", "description"}
        if extra_fields:
            raise serializers.ValidationError(
                f"Only 'rating' and 'description' may be changed, not: {', '.join(extra_fields)}."
            )
        return attrs
