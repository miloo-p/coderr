from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsBusinessOrReadOnly(BasePermission):
    """
    Allows access to business functions.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.type == "business"


class IsCreatorOfOffer(BasePermission):
    """
    Allows access to an offer only for its creator.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
