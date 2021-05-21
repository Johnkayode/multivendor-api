from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, BasePermission


class IsVendor(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and \
                request.user.is_confirmed and request.user.user_type == 'VENDOR'
        )
