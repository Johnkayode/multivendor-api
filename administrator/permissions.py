from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, BasePermission


class IsSuperuser(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated \
                and request.user.superuser_status
        )

class CustomerAccessPermission(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        ...