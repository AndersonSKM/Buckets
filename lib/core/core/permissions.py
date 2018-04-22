from rest_framework import permissions


class AnonCreateUserUpdateSelfOnly(permissions.BasePermission):
    """
    Custom permission:
        - allow anonymous CREATE
        - allow authenticated GET, PUT, DELETE on self record
        - allow all actions for staff
    """

    def has_permission(self, request, view):
        return (
            view.action == 'create'
            or (request.user and request.user.is_authenticated)
        )

    def has_object_permission(self, request, view, obj):
        SAFE_ACTIONS = ['retrieve', 'update', 'partial_update', 'destroy']
        return (
            view.action in SAFE_ACTIONS
            and obj.id == request.user.id
            or request.user.is_admin
        )


class ListUserAdminOnly(permissions.BasePermission):
    """
    Custom permission to only allow access to lists for admins
    """

    def has_permission(self, request, view):
        return (
            (view.action != 'list')
            or (request.user and request.user.is_admin)
        )
