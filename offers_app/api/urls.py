from django.urls import path

from .views import OfferDetailView, OfferView

urlpatterns = [
    path("offers/", OfferView.as_view(), name="offers"),
    path("offers/<int:pk>/", OfferDetailView.as_view(), name="offer-detail"),
]
