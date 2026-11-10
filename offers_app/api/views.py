from django.db.models import Min, Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from offers_app.models import Offer, OfferDetail

from .permissions import IsBusinessOrReadOnly, IsCreatorOfOffer
from .serializers import (
    OfferDetailSerializer,
    OfferFilterSerializer,
    OfferListSerializer,
    OfferRetrieveSerializer,
    OfferSerializer,
)


class OfferPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = "page_size"


def get_offers_with_min_values():
    return Offer.objects.annotate(
        min_price=Min("details__price"), min_delivery_time=Min("details__delivery_time_in_days")
    )


def filter_offers(offers, params):
    """
    Applies the validated query filters and the ordering to the offers.
    """
    if "creator_id" in params:
        offers = offers.filter(user_id=params["creator_id"])
    if "max_delivery_time" in params:
        offers = offers.filter(min_delivery_time__lte=params["max_delivery_time"])
    if "min_price" in params:
        offers = offers.filter(min_price__gte=params["min_price"])
    if "search" in params:
        search = params["search"]
        offers = offers.filter(Q(title__icontains=search) | Q(description__icontains=search))
    return offers.order_by(params.get("ordering", "-updated_at"))


class OfferView(APIView):
    """
    View for a new offer or offer list.
    """

    permission_classes = [IsBusinessOrReadOnly]

    def post(self, request):
        """
        Creates a new offer and returns the offer data.
        """
        serializer = OfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        Returns the filtered, ordered and paginated list of offers.
        """
        filter_serializer = OfferFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        offers = filter_offers(get_offers_with_min_values(), filter_serializer.validated_data)
        paginator = OfferPagination()
        page = paginator.paginate_queryset(offers, request)
        serializer = OfferListSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)


class OfferRetrieveView(APIView):
    permission_classes = [IsAuthenticated, IsCreatorOfOffer]

    def get(self, request, pk):
        """
        Returns a single offer.
        """
        queryset = get_offers_with_min_values()
        offer = get_object_or_404(queryset, pk=pk)
        serializer = OfferRetrieveSerializer(offer, context={"request": request})
        return Response(serializer.data)

    def delete(self, request, pk):
        """
        Deletes a single offer.
        """
        offer = get_object_or_404(Offer, pk=pk)
        self.check_object_permissions(request, offer)
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        """
        Updates offer values (partial allowed).
        """
        offer = get_object_or_404(Offer, pk=pk)
        self.check_object_permissions(request, offer)
        serializer = OfferSerializer(offer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class OfferDetailRetrieveView(APIView):
    def get(self, request, pk):
        """
        Returns infos for a single OfferDetail.
        """
        offer_detail = get_object_or_404(OfferDetail, pk=pk)
        serializer = OfferDetailSerializer(offer_detail)
        return Response(serializer.data)
