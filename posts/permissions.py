from rest_framework import permissions

#cutom permission setting

class IsOwnerPermission(permissions.BasePermission):
    #inherits from BasePermission
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
