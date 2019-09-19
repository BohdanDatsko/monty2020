from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from monty.models import Dictionary, Theme, Word


class IsLoggedInUserOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff


class IsUserAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff


class IsDictOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        else:
            if request.user.is_anonymous:
                raise PermissionDenied()
            view.queryset = Dictionary.objects.filter(owner=request.user.profile)
            if len(view.queryset) == 0:
                return True
            return view.queryset

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user.profile or request.user.is_staff


class IsThemeOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        else:
            view.queryset = Theme.objects.filter(dictionary__owner=request.user.profile)
            if len(view.queryset) == 0:
                return True
            return view.queryset

    def has_object_permission(self, request, view, obj):
        return request.user.profile == obj.get_user()


class IsWordOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        else:
            view.queryset = Word.objects.filter(
                dictionary__owner=request.user.profile
            )
            if len(view.queryset) == 0:
                return True
            return view.queryset

    def has_object_permission(self, request, view, obj):
        return request.user.profile == obj.get_user()
