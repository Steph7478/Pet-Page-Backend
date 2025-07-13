from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from users.serializers.loginSerializer import EmailTokenObtainPairSerializer

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