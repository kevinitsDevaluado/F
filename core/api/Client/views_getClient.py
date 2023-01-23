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
from core.api.Client.serializers_client import UserSerializer, ClientSerializer

class ClientGetViewSet(viewsets.GenericViewSet):
    model = User
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def list(self,request):
        users_serializer = self.get_serializer(self.queryset, many=True)
        return Response(users_serializer.data, status = status.HTTP_200_OK)

    def create(self,request):
        users_serializer = UserSerializer(data=request.data)
        if users_serializer.is_valid():
            email = request.data['email']
            users_serializer.save()
            id_cli = User.objects.get(id = users_serializer.data['id'])
            id_cli.email = email
            id_cli.save()
            mobile = request.data['mobile']
            address = request.data['address']
            Client.objects.create(user=id_cli,mobile=mobile,address=address)
            self.send_email(id_cli.id)
            return Response({'message':'Usuario creado correctamente'}, status = status.HTTP_201_CREATED)
        return Response( users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        clientList = Client.objects.filter(user_id = pk).first()
        if clientList:
            clientSerializers = ClientSerializer(clientList)
            return Response(clientSerializers.data, status = status.HTTP_200_OK)
        return Response({"message":"No hay clientes"}, status = status.HTTP_400_BAD_REQUEST)
    