from rest_framework.permissions import BasePermission


class IsBusinessTypeProfile(BasePermission):
    """
    Allows access to business functions.
    """

    def has_permission(self, request, view):
        return request.user.type == "business"
