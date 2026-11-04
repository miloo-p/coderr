from django.urls import path

from .views import OfferDetailRetrieveView, OfferRetrieveView, OfferView

urlpatterns = [
    path("offers/", OfferView.as_view(), name="offers"),
    path("offerdetails/<int:pk>/", OfferDetailRetrieveView.as_view(), name="offerdetail-infos"),
    path("offers/<int:pk>/", OfferRetrieveView.as_view(), name="offer-detail"),
]
