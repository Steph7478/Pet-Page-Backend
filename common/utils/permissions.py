from rest_framework.permissions import BasePermission

class DenyAllPermission(BasePermission):
    def has_permission(self, request, view):
        return False

def get_permissions_by_method(request_method, get_perm=None, post_perm=None, put_perm=None, patch_perm=None, delete_perm=None):
    default_permission = DenyAllPermission

    mapping = {
        'GET': get_perm or default_permission,
        'POST': post_perm or default_permission,
        'PUT': put_perm or default_permission,
        'PATCH': patch_perm or default_permission,
        'DELETE': delete_perm or default_permission,
    }

    perm_class = mapping.get(request_method, default_permission)
    return [perm_class()]
