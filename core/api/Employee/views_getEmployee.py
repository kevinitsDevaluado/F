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
from core.api.Employee.serializers_employee import *

class EmployeeViewSet(viewsets.GenericViewSet):
    model = Employee
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.all()
        return self.queryset
    
    def list(self,request):
        employee = self.get_queryset()
        if employee:
            employee_serializer = self.serializer_class(employee,many=True)
            return Response(employee_serializer.data, status = status.HTTP_200_OK)
        return Response({"message":"No hay ninguna usuario"}, status = status.HTTP_400_BAD_REQUEST)