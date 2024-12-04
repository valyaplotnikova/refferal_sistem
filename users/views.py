import random
import time

from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import User
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny


class SendAuthCode(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get_or_create(phone_number=phone_number)
        user.save()
        time.sleep(random.uniform(1, 2))
        return Response({'message': 'Code sent successfully'})


class VerifyAuthCode(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        auth_code = request.data.get('auth_code')

        if not phone_number or not auth_code:
            return Response({'error': 'Phone number and auth code are required'}, status=status.HTTP_400_BAD_REQUEST)

        if phone_number and auth_code:
            user = authenticate(phone_number=phone_number, auth_code=auth_code)
            if user:
                return Response({'message': 'Authentication successful'})
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Invalid auth code'}, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    """Информация о пользователях."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    @action(methods=('GET',), detail=False,
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status.HTTP_200_OK)


class ActivateInvitation(APIView):
    def put(self, request):
        phone_number = request.data.get('phone_number')
        invitation_code = request.data.get('invitation_code')

        if not phone_number or not invitation_code:
            return Response(
                {'error': 'Phone number and invitation code are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(phone_number=phone_number)
            user.activated_invitation_code = invitation_code
            user.save()
            return Response({'message': 'Invitation activated'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
