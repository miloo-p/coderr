from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsCustomerOrReadOnly
from .serializers import OrderSerializer


class OrderView(APIView):
    """
    View for an order.
    """

    permission_classes = [IsAuthenticated, IsCustomerOrReadOnly]

    def post(self, request):
        """
        Creates a new order and returns the order data.
        """
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(customer_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
