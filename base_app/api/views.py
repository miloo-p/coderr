from django.db.models import Avg
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.models import CoderrUser
from offers_app.models import Offer
from reviews_app.models import Review


class BaseInfoView(APIView):
    """
    Returns general statistics about the platform.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        """
        Returns review count, average rating, business profile count and offer count.
        """
        average_rating = Review.objects.aggregate(average=Avg("rating"))["average"] or 0
        return Response(
            {
                "review_count": Review.objects.count(),
                "average_rating": round(average_rating, 1),
                "business_profile_count": CoderrUser.objects.filter(type="business").count(),
                "offer_count": Offer.objects.count(),
            }
        )
