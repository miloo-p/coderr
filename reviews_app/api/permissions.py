from rest_framework.permissions import BasePermission


class IsReviewer(BasePermission):
    """
    Allows changing or deleting a review only for the customer who wrote it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.reviewer == request.user
