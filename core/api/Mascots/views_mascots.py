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
from core.api.Mascots.serializers_mascots import *


class MascotsViewSet(viewsets.GenericViewSet):
    model = Mascots
    serializer_class = MascotsSerializer
    queryset = Mascots.objects.all()

    def list(self,request):
        historial_serializer = self.get_serializer(self.queryset, many=True)
        return Response(historial_serializer.data, status = status.HTTP_200_OK)

    def create(self,request):
        mascots_serializer = MascotsSerializer(data=request.data)
        if mascots_serializer.is_valid():
            mascots_serializer.save()
            return Response({'message':'Mascota creado correctamente'}, status = status.HTTP_201_CREATED)
        return Response( mascots_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_object(self,pk):
        return get_object_or_404(Mascots, client_id=pk)
    
    def retrieve(self, request, pk=None):
        mascot = self.get_object(pk)
        mmascots_serializer = MascotsSerializer(mascot)
        return Response([mmascots_serializer.data], status = status.HTTP_200_OK)
