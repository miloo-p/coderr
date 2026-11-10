from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders_app.api.permissions import IsCustomerOrReadOnly

from ..models import Review
from .permissions import IsReviewer
from .serializers import ReviewFilterSerializer, ReviewSerializer, ReviewUpdateSerializer


class ReviewView(APIView):
    """
    Lists reviews and lets customers create one.
    """

    permission_classes = [IsAuthenticated, IsCustomerOrReadOnly]

    def get(self, request):
        """
        Returns all reviews, optionally filtered and ordered.
        """
        filters = ReviewFilterSerializer(data=request.query_params)
        filters.is_valid(raise_exception=True)
        params = filters.validated_data
        reviews = Review.objects.all()
        if "business_user_id" in params:
            reviews = reviews.filter(business_user_id=params["business_user_id"])
        if "reviewer_id" in params:
            reviews = reviews.filter(reviewer_id=params["reviewer_id"])
        if "ordering" in params:
            reviews = reviews.order_by(params["ordering"])
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Creates a review of a business user by the logged-in customer.
        """
        serializer = ReviewSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(reviewer=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewDetailView(APIView):
    """
    Lets the reviewer update or delete a single review.
    """

    permission_classes = [IsAuthenticated, IsReviewer]

    def patch(self, request, pk):
        """
        Updates rating and/or description and returns the whole review.
        """
        review = get_object_or_404(Review, pk=pk)
        self.check_object_permissions(request, review)
        serializer = ReviewUpdateSerializer(review, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ReviewSerializer(review).data)

    def delete(self, request, pk):
        """
        Deletes a review.
        """
        review = get_object_or_404(Review, pk=pk)
        self.check_object_permissions(request, review)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
