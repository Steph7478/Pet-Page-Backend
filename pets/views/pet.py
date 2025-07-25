import traceback
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.database.supabase import supabase
from common.utils.filter import filtrar_e_listar
from common.utils.permissions import DenyAllPermission, get_permissions_by_method
from pets.models.petInfo import Pet
from pets.serializers.petInfoSerializer import PetSerializer
from rest_framework.permissions import AllowAny
from api.docs.doc import document_api
from rest_framework.permissions import IsAuthenticated


class PetView(APIView):
    def get_permissions(self):
        return get_permissions_by_method(
            self.request.method,
            get_perm=AllowAny,
            post_perm=IsAuthenticated,
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

        file_bytes = file.read()

        result = supabase.storage.from_("pets-avatar").upload(
            path,
            file_bytes,
            {"content-type": file.content_type}
        )

        error = None
        if hasattr(result, "error") and result.error:
            error = result.error
        elif isinstance(result, dict) and result.get("error"):
            error = result["error"]
        elif hasattr(result, "status_code") and result.status_code >= 400:
            error = f"Upload falhou com status {result.status_code}"

        if error:
            raise Exception(f"Erro ao fazer upload no Supabase: {error}")

        public_url = supabase.storage.from_("pets-avatar").get_public_url(path)
        return public_url


    @document_api(PetSerializer, summary="Adicionar pet", request_body=True)
    def post(self, request):
        try:
            data = request.data.copy()
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
