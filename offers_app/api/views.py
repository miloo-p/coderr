from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsBusinessTypeProfile
from .serializers import OfferSerializer


class OfferView(APIView):
    """
    View for a new Offer.
    """

    permission_classes = [IsAuthenticated, IsBusinessTypeProfile]

    def post(self, request):
        """
        Creates a new offer and returns the offer data.
        """
        serializer = OfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
