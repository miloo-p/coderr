from django.conf import settings
from django.db import models


class Offer(models.Model):
    """
    Offer related to a CoderrUser and its details.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="offers"
    )
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="uploads/offers/", blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Offer"
        verbose_name_plural = "Offers"

    def __str__(self):
        """
        Shows the title, e.g. in the admin.
        """
        return self.title


class OfferDetail(models.Model):
    """
    Offer details related to an Offer.
    """

    OFFER_TYPE_CHOICES = [
        ("basic", "basic"),
        ("standard", "standard"),
        ("premium", "premium"),
    ]
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="details")
    title = models.CharField(max_length=100)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()
    offer_type = models.CharField(max_length=8, choices=OFFER_TYPE_CHOICES)

    class Meta:
        ordering = ["id"]
        verbose_name = "Offer detail"
        verbose_name_plural = "Offer details"

    def __str__(self):
        """
        Shows offer title and package type, e.g. in the admin.
        """
        return f"{self.offer.title} ({self.offer_type})"
