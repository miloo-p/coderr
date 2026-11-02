from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOfProfile(BasePermission):
    """
    Allows access to a profile only for its owner.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj == request.user
