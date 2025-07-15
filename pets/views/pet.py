import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.database import supabase
from pets.models.petInfo import Pet
from pets.serializers.petInfoSerializer import PetSerializer
from rest_framework.permissions import AllowAny
from api.docs.doc import document_api

class PetView(APIView):
    permission_classes = [AllowAny]

    def _upload_to_supabase(self, file):
        ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]
        file_ext = file.name.split('.')[-1].lower()
        
        if file_ext not in ALLOWED_EXTENSIONS:
            raise Exception(f"Extensão '{file_ext}' não permitida.")

        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        path = f"pets/{unique_filename}"

        result = supabase.storage.from_("pets-avatar").upload(path, file, file.content_type)

        if result.get("error"):
            raise Exception(result["error"]["message"])

        public_url = supabase.storage.from_("pets-avatar").get_public_url(path)
        return public_url
    
    @document_api(PetSerializer, summary="Adicionar pet", request_body=True)
    def post(self, request):
        try:
            foto = request.FILES.get('fotoUrl')
            data = request.data.copy()
            data['status'] = 'disponivel'

            if foto:
                foto_url = self._upload_to_supabase(foto)
                data['fotoUrl'] = foto_url
            else:
                if not data.get('fotoUrl'):
                  return Response(
                    {"fotoUrl": ["Este campo é obrigatório. Envie uma URL ou faça upload de uma imagem."]},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = PetSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @document_api(PetSerializer, Pet, summary="Listar pets")
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

        try:
            if filters:
                pets = Pet.objects.filter(**filters)
                if not pets.exists():
                    return Response({'detail': 'Nenhum pet encontrado.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                pets = Pet.objects.all()

            serializer = PetSerializer(pets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
