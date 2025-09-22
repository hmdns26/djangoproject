from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS or (request.user and request.user.is_staff))

class SendPrivateToCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('store.send_private_email'))

import copy

class CustomDjangoModelPermission(permissions.DjangoModelPermissions):
    def __init__(self):
        self.perms_map=copy.deepcopy(self.perms_map)
        self.perms_map['GET']==['%(app_label)s.view_%(model_name)s']