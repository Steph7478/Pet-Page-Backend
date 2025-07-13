from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from adoption.models.allowAdoption import AllowAdoption, PetAdoption
from adoption.serializers.allowAdoptionSerializer import AllowAdoptionSerializer
from pets.models.petInfo import Pet
from django.utils.dateparse import parse_date

class AllowAdoptionView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def post(self, request):
        client_id = request.data.get('clientId')
        pet_ids = request.data.get('petId', [])

        if not client_id:
            return Response({"error": "clientId is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(pet_ids, (list, tuple)):
            pet_ids = [pet_ids]

        adoption, _ = AllowAdoption.objects.get_or_create(clientId_id=client_id)

        for pet_id in pet_ids:
            try:
                pet = Pet.objects.get(petId=pet_id)
            except Pet.DoesNotExist:
                return Response({"error": f"Pet com id {pet_id} não existe"}, status=status.HTTP_400_BAD_REQUEST)

            pet.status = 'adotado'
            pet.save()

            PetAdoption.objects.get_or_create(adoption=adoption, pet=pet)

        serializer = AllowAdoptionSerializer(adoption)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        filters = {}
        valid_fields = [f.name for f in Pet._meta.fields]

        for key, value in request.query_params.items():
            if key in valid_fields:
                field = Pet._meta.get_field(key)
                internal_type = field.get_internal_type()

                if internal_type in ["CharField", "TextField"]:
                    filters[f"{key}__icontains"] = value
                else:
                    filters[key] = value

        client_id = request.query_params.get('clientId')
        data_inicio = parse_date(request.query_params.get('data_inicio', ''))
        data_fim = parse_date(request.query_params.get('data_fim', ''))

        try:
            if filters:
                pets = Pet.objects.filter(**filters)
                if not pets.exists():
                    return Response({'detail': 'Nenhum pet encontrado com os filtros aplicados.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                pets = Pet.objects.all()

            adoptions = AllowAdoption.objects.filter(pet_links__pet__in=pets)

            if client_id:
                adoptions = adoptions.filter(clientId_id=client_id)

            if data_inicio and data_fim:
                adoptions = adoptions.filter(pet_links__dataAdocao__range=[data_inicio, data_fim])

            adoptions = adoptions.distinct()

            if not adoptions.exists():
                return Response({'detail': 'Nenhuma adoção encontrada com os filtros aplicados.'}, status=status.HTTP_404_NOT_FOUND)

            serializer = AllowAdoptionSerializer(adoptions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
