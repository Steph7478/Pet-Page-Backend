from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def refresh_token(request):
    refresh_token = request.COOKIES.get('refresh_token')

    if refresh_token is None:
        return Response({'detail': 'Refresh token not found in cookies.'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        token = RefreshToken(refresh_token)
        new_access_token = str(token.access_token)

        response = Response({'detail': 'Access token refreshed.'}, status=status.HTTP_200_OK)

        response.set_cookie(
            key='access_token',
            value=new_access_token,
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=15 * 60
        )

        return response

    except TokenError:
        return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_401_UNAUTHORIZED)