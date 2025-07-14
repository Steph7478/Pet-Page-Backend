from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
    

