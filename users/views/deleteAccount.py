from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

class DeleteAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"detail": "Conta excluída com sucesso."}, status=status.HTTP_204_NO_CONTENT)
