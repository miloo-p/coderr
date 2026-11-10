from django.urls import path

from .views import OrderDetailView, OrderView

urlpatterns = [
    path("orders/", OrderView.as_view(), name="orders"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="orders-detail"),
]
