from rest_framework import permissions


class GeneralPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and (request.user.is_staff or request.user.role == 'admin')
            or request.method in permissions.SAFE_METHODS
        )


class IsAuthorModerAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role == 'moderator'
                or request.user.role == 'admin'):
            return True


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            (request.user.is_authenticated)
            and (request.user.is_superuser or request.user.role == 'admin')
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
