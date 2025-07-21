from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from api.docs.doc import document_api
from api.docs.params import generate_cookie_auth_param
from api.middlewares.cookies import CookieJWTAuthentication
from common.utils import DenyAllPermission, get_permissions_by_method
from users.serializers.auth import LoginSerializer, RegisterSerializer

class LoginView(APIView):
    def get_permissions(self):
        return get_permissions_by_method(
            self.request.method,
            get_perm=DenyAllPermission,
            post_perm=IsAuthenticated,
            put_perm=DenyAllPermission,
            patch_perm=DenyAllPermission,
            delete_perm=DenyAllPermission,
        )

    @document_api(LoginSerializer, summary="Iniciar sessão", request_body=True)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            refresh = serializer.validated_data['refresh']
            access = serializer.validated_data['access']

            response = Response(status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=str(access),
                httponly=True,
                secure=True,
                samesite='None',
                max_age=15*60,
                path='/'
            )
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='None',
                max_age=7 * 24 * 60 * 60,
                path='/'
            )
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutView(APIView):
    def get_permissions(self):
        return get_permissions_by_method(
            self.request.method,
            get_perm=DenyAllPermission,
            post_perm=IsAuthenticated,
            put_perm=DenyAllPermission,
            patch_perm=DenyAllPermission,
            delete_perm=DenyAllPermission,
        )
    authentication_classes = [CookieJWTAuthentication]

    @document_api(summary="Finalizar sessão", request_body=True, security=[{"RefreshCookieAuth": []}], manual_parameters=[generate_cookie_auth_param(cookie_name="refresh_token")])
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass

        response = Response({'detail': 'Logged out.'}, status=status.HTTP_200_OK)

        for cookie in ['access_token', 'refresh_token']:
            response.set_cookie(
                key=cookie,
                value='',
                max_age=0,
                path='/',
                secure=True,
                httponly=True,
                samesite='None'
            )

        return response


class RegisterView(APIView):
    def get_permissions(self):
        return get_permissions_by_method(
            self.request.method,
            get_perm=IsAuthenticated,
            post_perm=AllowAny,
            put_perm=DenyAllPermission,
            patch_perm=DenyAllPermission,
            delete_perm=DenyAllPermission,
        )

    @document_api(RegisterSerializer, summary="Cadastrar", request_body=True)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token_serializer = LoginSerializer(data={
                'email': request.data.get('email'),
                'password': request.data.get('password')
            })

            if token_serializer.is_valid():
                refresh = token_serializer.validated_data['refresh']
                access = token_serializer.validated_data['access']

                user_response = RegisterSerializer(user).data

                response = Response(user_response, status=status.HTTP_201_CREATED)
                response.set_cookie(
                    key='access_token',
                    value=str(access),
                    httponly=True,
                    secure=True,
                    samesite='None',
                    max_age=15 * 60,
                    path='/'
                )
                response.set_cookie(
                    key='refresh_token',
                    value=str(refresh),
                    httponly=True,
                    secure=True,
                    samesite='None',
                    max_age=7 * 24 * 60 * 60,
                    path='/'
                )
                return response

            return Response(token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountView(APIView):
    def get_permissions(self):
        return get_permissions_by_method(
            self.request.method,
            get_perm=DenyAllPermission,
            post_perm=DenyAllPermission,
            put_perm=DenyAllPermission,
            patch_perm=DenyAllPermission,
            delete_perm=IsAuthenticated,
        )

    @document_api(summary="Deletar Conta", request_body=True, security=[{"AccessCookieAuth": []}], manual_parameters=[generate_cookie_auth_param(cookie_name="access_token")])
    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"detail": "Conta excluída com sucesso."}, status=status.HTTP_204_NO_CONTENT)
