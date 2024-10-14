"""
Views for handling API requests for all the stuff with user.
"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone

from ..models import User
from ..serializers import UserSerializer


class TelegramRegisterView(generics.CreateAPIView):
    """
    Create a new user using JWT and data from telegram widget form
    """
    
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.save()
        
        return Response(tokens, status=status.HTTP_201_CREATED)


    
class GetUserView(generics.RetrieveAPIView):
    # def get(self, request, *args, **kwargs):
    #     serializer = UserSerializer(request.user)
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)
    queryset = User.objects.all()
    serializer_class = UserSerializer
