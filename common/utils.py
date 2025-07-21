from rest_framework.response import Response
from rest_framework import status
from django.db.models import Model
from rest_framework.permissions import BasePermission

class DenyAllPermission(BasePermission):
    def has_permission(self, request, view):
        return False


def filtrar_e_listar(request, model: Model, serializer_class, not_found_message="Nenhum item encontrado com os filtros aplicados."):
    try:
        filters = {}
        valid_fields = [f.name for f in model._meta.get_fields() if hasattr(f, 'get_internal_type')]

        for key, value in request.query_params.items():
            if key in valid_fields:
                field = model._meta.get_field(key)
                internal_type = field.get_internal_type()

                if internal_type in ["CharField", "TextField"]:
                    filters[f"{key}__icontains"] = value
                else:
                    filters[key] = value

        queryset = model.objects.filter(**filters) if filters else model.objects.all()

        if not queryset.exists():
            return Response(
                {"detail": not_found_message},
                status=status.HTTP_404_NOT_FOUND
            )

        serialized = serializer_class(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"detail": "Erro ao filtrar dados.", "error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

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
