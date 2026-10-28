from django.contrib.auth.models import AbstractUser
from django.db import models


class CoderrUser(AbstractUser):
    TYPE_CHOICES = [
        ("customer", "customer"),
        ("business", "business"),
    ]

    file = models.ImageField(upload_to="uploads/", blank=True)
    location = models.CharField(max_length=50, blank=True)
    tel = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=50, blank=True)
    type = models.CharField(choices=TYPE_CHOICES, blank=False, max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
