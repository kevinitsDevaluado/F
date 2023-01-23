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
from core.clinic.models import *
from core.api.Client.serializers_client import UserSerializer, ClientSerializer
from core.api.HistorialMedical.serializers_historial import *
class HistorialViewSet(viewsets.GenericViewSet):
    model = Sale
    serializer_class = HistorialSerializer
    queryset = Sale.objects.all()

    def list(self,request):
        historial_serializer = self.get_serializer(self.queryset, many=True)
        return Response(historial_serializer.data, status = status.HTTP_200_OK)

    def create(self,request):
        users_serializer = UserSerializer(data=request.data)
        if users_serializer.is_valid():
            users_serializer.save()
            return Response({'message':'Usuario creado correctamente'}, status = status.HTTP_201_CREATED)
        return Response( users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_object(self,pk):
        return get_object_or_404(Sale, id=pk)
    
    def retrieve(self, request, pk=None):
        historial = self.get_object(pk)
        historial_serializer = HistorialSerializer(historial)
        return Response([historial_serializer.data], status = status.HTTP_200_OK)
