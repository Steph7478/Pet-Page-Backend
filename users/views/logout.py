from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status
from api.middlewares.cookies import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated

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
