import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from config import settings
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from core.user.models import User
from core.clinic.models import Client
from core.api.Client.serializers_client import ClientSerializer
from core.api.User.serializers_user import *
class UserGetViewSet(viewsets.GenericViewSet):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self,request):
        users_serializer = self.get_serializer(self.queryset, many=True)
        return Response(users_serializer.data, status = status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        clientList = User.objects.filter(id = pk).first()
        if clientList:
            clientSerializers = UserSerializer(clientList)
            return Response(clientSerializers.data, status = status.HTTP_200_OK)
        return Response({"message":"No hay clientes"}, status = status.HTTP_400_BAD_REQUEST)
    