from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.docs.doc import document_api
from api.docs.params import generate_cookie_auth_param
from api.middlewares.cookies import CookieJWTAuthentication
from users.serializers.userInfoSerializer import UserSerializer

class MeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    @document_api(summary="Informações do usuário", request_body=True, security=[{"AccessCookieAuth": []}], manual_parameters=[generate_cookie_auth_param(cookie_name="access_token")])
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
