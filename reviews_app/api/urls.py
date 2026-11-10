from django.urls import path

from .views import ReviewDetailView, ReviewView

urlpatterns = [
    path("reviews/", ReviewView.as_view(), name="reviews"),
    path("reviews/<int:pk>/", ReviewDetailView.as_view(), name="review-detail"),
]
