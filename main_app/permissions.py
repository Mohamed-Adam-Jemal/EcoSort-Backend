from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow read-only access to everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow write access only to admin users
        return request.user and request.user.is_staff