from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsCustomerOrReadOnly(BasePermission):
    """
    Allows access to customer functions.
    """

    def has_permission(self, request, view):
        """
        Everyone may read, only customers may create.
        """
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.type == "customer"


class IsCreatorOfOrder(BasePermission):
    """
    Business user of the order may update it, only staff may delete it.
    """

    def has_object_permission(self, request, view, obj):
        """
        Only staff may delete, only the business user of the order may update.
        """
        if request.method == "DELETE":
            return request.user.is_staff
        return obj.business_user == request.user
