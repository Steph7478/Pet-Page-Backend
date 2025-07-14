from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from api.middlewares.cookies import CookieJWTAuthentication
from users.serializers.auth import EmailTokenObtainPairSerializer, RegisterSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailTokenObtainPairSerializer(data=request.data)
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
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

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
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token_serializer = EmailTokenObtainPairSerializer(data={
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
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"detail": "Conta excluída com sucesso."}, status=status.HTTP_204_NO_CONTENT)
