import traceback
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.database import supabase
from common.utils.filter import filtrar_e_listar
from common.utils.permissions import DenyAllPermission, get_permissions_by_method
from pets.models.petInfo import Pet
from pets.serializers.petInfoSerializer import PetSerializer
from rest_framework.permissions import AllowAny
from api.docs.doc import document_api


class PetView(APIView):
    def get_permissions(self):
        return get_permissions_by_method(
            self.request.method,
            get_perm=AllowAny,
            post_perm=AllowAny,
            put_perm=DenyAllPermission,
            patch_perm=DenyAllPermission,
            delete_perm=DenyAllPermission,
        )

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
            data = request.data.copy()
            data['status'] = 'disponivel'

            foto = request.FILES.get('fotoUrl')

            if foto:
                foto_url = self._upload_to_supabase(foto)
                data['fotoUrl'] = foto_url
            else:
                foto_url_str = data.get('fotoUrl')
                if not foto_url_str:
                    return Response(
                        {"fotoUrl": ["Este campo é obrigatório. Envie uma URL ou faça upload de uma imagem."]},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                data['fotoUrl'] = foto_url_str

            serializer = PetSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(traceback.format_exc())
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @document_api(PetSerializer, Pet, summary="Listar pets")
    def get(self, request):
        return filtrar_e_listar(
            request=request,
            model=Pet,
            serializer_class=PetSerializer,
            not_found_message="Nenhum pet encontrado."
        )
