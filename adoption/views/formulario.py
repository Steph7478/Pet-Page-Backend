from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from adoption.models.formulario import Formulario
from adoption.serializers.formularioSerializer import FormularioSerializer
from rest_framework import permissions
from api.docs.doc import document_api
from api.docs.params import generate_cookie_auth_param

class FormularioView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @document_api(FormularioSerializer, summary="Criar Formulário", request_body=True, security=[{"AccessCookieAuth": []}], manual_parameters=[generate_cookie_auth_param(cookie_name="access_token")])
    def post(self, request):
        serializer = FormularioSerializer(data=request.data)

        if serializer.is_valid():
            formulario = serializer.save()

            pet = formulario.petId 
            pet.status = 'pendente'
            pet.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @document_api(FormularioSerializer, Formulario, summary="Listar Formulários", security=[{"AccessCookieAuth": []}], manual_parameters=[generate_cookie_auth_param(cookie_name="access_token")])
    def get(self, request):
        filters = {}
        valid_fields = [f.name for f in Formulario._meta.fields]

        for key, value in request.query_params.items():
            if key in valid_fields:
                field = Formulario._meta.get_field(key)
                internal_type = field.get_internal_type()

                if internal_type in ["CharField", "TextField"]:
                    filters[f"{key}__icontains"] = value
                else:
                    filters[key] = value

        try:
            if filters:
                form = Formulario.objects.filter(**filters)
                if not form.exists():
                    return Response(
                        {'detail': 'Nenhum formulário encontrado com os filtros aplicados.'},
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                form = Formulario.objects.all()

            serializer = FormularioSerializer(form, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'detail': 'Erro ao filtrar formulários.', 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
