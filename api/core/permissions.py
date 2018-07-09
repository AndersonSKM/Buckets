from django.db.models import Model
from django.http import HttpRequest
from rest_framework import permissions
from rest_framework.viewsets import ViewSet


class AllowAnyCreateUpdateIsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission:
        - allow anonymous CREATE
        - allow authenticated GET, PUT, DELETE on self record
        - allow all actions for staff
    """

    def has_permission(self, request: HttpRequest, view: ViewSet) -> bool:
        return (
            view.action == 'create' or
            (request.user and request.user.is_authenticated)
        )

    def has_object_permission(self, request: HttpRequest, view: ViewSet, obj: Model) -> bool:
        safe_actions = ['retrieve', 'update', 'partial_update', 'destroy']
        return (
            view.action in safe_actions and
            obj.id == request.user.id or
            request.user.is_staff
        )


class AllowListIsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow access to lists for admins
    """

    def has_permission(self, request: HttpRequest, view: ViewSet) -> bool:
        return (
            (view.action != 'list') or
            (request.user and request.user.is_staff)
        )
