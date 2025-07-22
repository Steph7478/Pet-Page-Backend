from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from adoption.models.formulario import Formulario
from adoption.serializers.formularioSerializer import FormularioSerializer
from rest_framework.permissions import IsAuthenticated
from api.docs.doc import document_api
from api.docs.params import generate_cookie_auth_param
from common.utils.filter import filtrar_e_listar
from common.utils.permissions import DenyAllPermission, get_permissions_by_method

class FormularioView(APIView):
    def get_permissions(self):
        return get_permissions_by_method(
            self.request.method,
            get_perm=IsAuthenticated,
            post_perm=IsAuthenticated,
            put_perm=DenyAllPermission,
            patch_perm=DenyAllPermission,
            delete_perm=DenyAllPermission,
        )

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
        return filtrar_e_listar(
            request=request,
            model=Formulario,
            serializer_class=FormularioSerializer,
            not_found_message="Nenhum formulário encontrado com os filtros aplicados."
        )