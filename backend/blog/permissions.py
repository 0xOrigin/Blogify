from rest_framework import permissions
from core.permissions import BasePermissions


class BlogPermissions(BasePermissions):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author.id == request.user.id
