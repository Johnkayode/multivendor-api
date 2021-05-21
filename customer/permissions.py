from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, BasePermission


class IsCustomer(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated \
                and request.user.is_confirmed and request.user.user_type == 'CUSTOMER'
        )

class CustomerAccessPermission(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        ...