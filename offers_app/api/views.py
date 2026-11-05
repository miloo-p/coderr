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
        Returns a list of all offers.
        """
        offers = get_offers_with_min_values()
        serializer = OfferFilterSerializer(data=request.query_params)
        if serializer.is_valid():
            ordering = request.query_params.get("ordering")
            if ordering:
                offers = offers.order_by(ordering)
            else:
                offers = offers.order_by("-updated_at")
            creator_id = request.query_params.get("creator_id")
            if creator_id:
                offers = offers.filter(user_id=creator_id)
            max_delivery_time = request.query_params.get("max_delivery_time")
            if max_delivery_time:
                offers = offers.filter(min_delivery_time__lte=max_delivery_time)
            min_price = request.query_params.get("min_price")
            if min_price:
                offers = offers.filter(min_price__gte=min_price)
            search = request.query_params.get("search")
            if search:
                offers = offers.filter(
                    Q(title__icontains=search) | Q(description__icontains=search)
                )
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

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
