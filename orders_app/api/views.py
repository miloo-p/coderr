from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.models import CoderrUser

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
    """
    Lets the business user update the status and staff delete an order.
    """

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


class BaseOrderCountView(APIView):
    """
    Counts the orders of a business user with a given status.
    """

    order_status = None
    response_key = None

    def get(self, request, business_user_id):
        """
        Returns the number of orders with this view's status.
        """
        business_user = get_object_or_404(CoderrUser, pk=business_user_id, type="business")
        count = business_user.business_orders.filter(status=self.order_status).count()
        return Response({self.response_key: count})


class OrderCountView(BaseOrderCountView):
    """
    Returns the number of running orders of a business user.
    """

    order_status = "in_progress"
    response_key = "order_count"


class CompletedOrderCountView(BaseOrderCountView):
    """
    Returns the number of completed orders of a business user.
    """

    order_status = "completed"
    response_key = "completed_order_count"
