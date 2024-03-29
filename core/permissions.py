from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    The request is authenticated as an admin, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )

class AdminReadOnly(BasePermission):
    """
    The request is authenticated as an admin and is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(request.method not in SAFE_METHODS and not (request.user and request.user.is_staff))