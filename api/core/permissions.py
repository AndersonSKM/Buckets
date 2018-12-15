from rest_framework import permissions


class AllowAnyCreateUpdateIsOwner(permissions.BasePermission):
    """Custom permission:
    - allow anonymous POST
    - allow authenticated users to GET, PUT, DELETE on self records
    """
    SAFE_OBJECT_ACTIONS = ['retrieve', 'update', 'partial_update', 'destroy']

    def has_permission(self, request, view):
        return (view.action == 'create') or (request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (view.action in self.SAFE_OBJECT_ACTIONS) and (obj.id == request.user.id)
