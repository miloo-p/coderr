from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Order
from .permissions import IsCreatorOfOrder, IsCustomerOrReadOnly
from .serializers import OrderSerializer, OrderStatusSerializer


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

    def get(self, request):
        """
        Returns infos for orders.
        """
        orders = Order.objects.filter(Q(customer_user=request.user) | Q(business_user=request.user))
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated, IsCreatorOfOrder]

    def patch(self, request, pk):
        """
        Updates order values (partial allowed).
        """
        order = get_object_or_404(Order, pk=pk)
        self.check_object_permissions(request, order)
        serializer = OrderStatusSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data)

    def delete(self, request, pk):
        """
        Deletes an order (staff only).
        """
        order = get_object_or_404(Order, pk=pk)
        self.check_object_permissions(request, order)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
