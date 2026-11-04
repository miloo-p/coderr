from django.db.models import Min
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from offers_app.models import Offer

from .permissions import IsBusinessTypeProfile
from .serializers import OfferRetrieveSerializer, OfferSerializer


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


class OfferDetailView(APIView):
    def get(self, request, pk):
        """
        Returns a single offer.
        """
        queryset = Offer.objects.annotate(
            min_price=Min("details__price"), min_delivery_time=Min("details__delivery_time_in_days")
        )
        offer = get_object_or_404(queryset, pk=pk)
        serializer = OfferRetrieveSerializer(offer)
        return Response(serializer.data)
