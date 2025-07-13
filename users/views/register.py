from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from users.serializers.loginSerializer import EmailTokenObtainPairSerializer
from users.serializers.registerSerializer import RegisterSerializer


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
