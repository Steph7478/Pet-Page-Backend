from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from adoption.models.adopt import Adoption, PetAdoption
from adoption.models.formulario import Formulario
from adoption.serializers.adopt import AdoptionSerializer, GetAdoptionSerializer
from api.docs.doc import document_api
from api.docs.params import generate_cookie_auth_param
from common.utils.filter import filtrar_e_listar
from common.utils.permissions import DenyAllPermission, get_permissions_by_method
from pets.models.petInfo import Pet
from django.utils.dateparse import parse_date
from rest_framework.exceptions import MethodNotAllowed
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from pets.serializers.petInfoSerializer import PetSerializer

class AdoptionView(APIView):
    def get_permissions(self):
        return get_permissions_by_method(
            self.request.method,
            get_perm=IsAuthenticated,
            post_perm=IsAuthenticated,
            put_perm=DenyAllPermission,
            patch_perm=DenyAllPermission,
            delete_perm=DenyAllPermission,
        )

    def handle_adoption(self, request, action):
        client_id = request.data.get('clientId')
        pet_ids = request.data.get('petId', [])

        if not client_id:
            return Response({"error": "clientId é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(pet_ids, (list, tuple)):
            pet_ids = [pet_ids]

        adoption, _ = Adoption.objects.get_or_create(clientId_id=client_id)

        for pet_id in pet_ids:
            try:
                pet = Pet.objects.get(petId=pet_id)
            except Pet.DoesNotExist:
                return Response({"error": f"Pet com id {pet_id} não existe"}, status=status.HTTP_400_BAD_REQUEST)

            if action == 'permitir':
                pet.status = 'adotado'
                pet.save()
                adoption.save()
                PetAdoption.objects.get_or_create(adoption=adoption, pet=pet)

            elif action in ('rejeitar', 'cancelar'):
                pet.status = 'disponivel'
                pet.save()
                Formulario.objects.filter(clientId=client_id, petId=pet_id).delete()
            
            if action in ('rejeitar', 'cancelar') and not PetAdoption.objects.filter(adoption=adoption).exists():
                adoption.delete()

        serializer = GetAdoptionSerializer(adoption)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @document_api(
        AdoptionSerializer,
        model=PetAdoption,
        summary="Listar Adoções",
        security=[{"AccessCookieAuth": []}],
        manual_parameters=[generate_cookie_auth_param(cookie_name="access_token")]
    )
    def get(self, request):
        pets_response = filtrar_e_listar(
            request=request,
            model=Pet,
            serializer_class=PetSerializer,
            not_found_message="Nenhum pet encontrado com os filtros aplicados."
        )

        if pets_response.status_code == 404:
            return pets_response

        pets_data = pets_response.data
        pet_ids = [pet['id'] for pet in pets_data]

        adoptions = Adoption.objects.filter(pet_links__pet__id__in=pet_ids)

        client_id = request.query_params.get('clientId')
        data_inicio = parse_date(request.query_params.get('data_inicio', ''))
        data_fim = parse_date(request.query_params.get('data_fim', ''))

        if client_id:
            adoptions = adoptions.filter(clientId_id=client_id)

        if data_inicio and data_fim:
            adoptions = adoptions.filter(pet_links__dataAdocao__range=[data_inicio, data_fim])

        adoptions = adoptions.distinct()

        if not adoptions.exists():
            return Response(
                {'detail': 'Nenhuma adoção encontrada com os filtros aplicados.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = GetAdoptionSerializer(adoptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApproveAdoptionView(AdoptionView):
    @swagger_auto_schema(auto_schema=None)
    def get(self, request, *args, **kwargs):
        raise MethodNotAllowed('GET')
     
    @document_api(
        AdoptionSerializer,
        summary="Permitir Adoção",
        request_body=True,
        security=[{"AccessCookieAuth": []}],
        manual_parameters=[generate_cookie_auth_param(cookie_name="access_token")]
    )
    def post(self, request):
        return super().handle_adoption(request, action='permitir')


class RejectAdoptionView(AdoptionView):
    @swagger_auto_schema(auto_schema=None)
    def get(self, request, *args, **kwargs):
        raise MethodNotAllowed('GET')
    
    @document_api(
        AdoptionSerializer,
        summary="Rejeitar Adoção",
        request_body=True,
        security=[{"AccessCookieAuth": []}],
        manual_parameters=[generate_cookie_auth_param(cookie_name="access_token")]
    )
    def post(self, request):
        return super().handle_adoption(request, action='rejeitar')
    
class CancelAdoptionView(AdoptionView):
    @swagger_auto_schema(auto_schema=None)
    def get(self, request, *args, **kwargs):
        raise MethodNotAllowed('GET')
    
    @document_api(
        AdoptionSerializer,
        summary="Cancelar Adoção",
        request_body=True,
        security=[{"AccessCookieAuth": []}],
        manual_parameters=[generate_cookie_auth_param(cookie_name="access_token")]
    )
    def post(self, request):
        return super().handle_adoption(request, action='cancelar')
