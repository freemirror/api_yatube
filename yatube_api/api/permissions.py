from rest_framework import permissions


class AuthorOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return request.user.is_authenticated
        return obj.author == request.user
