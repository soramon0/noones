from rest_framework import permissions


# TODO(karim): IsOwnerOrIsAdmin?
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the model data.
        return obj.user == request.user
