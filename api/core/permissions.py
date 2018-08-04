from rest_framework import permissions


class AllowAnyCreateUpdateIsOwner(permissions.BasePermission):
    """Custom permission:
    - allow anonymous CREATE
    - allow authenticated GET, PUT, DELETE on self record
    """
    def has_permission(self, request, view):
        return (view.action == 'create') or (request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            (view.action in ['retrieve', 'update', 'partial_update', 'destroy']) and
            (obj.id == request.user.id)
        )
