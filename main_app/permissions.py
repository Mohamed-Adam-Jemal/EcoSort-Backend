from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.upper() == 'ADMIN'

class IsAgent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.upper() == 'AGENT'

class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.upper() == 'USER'