from rest_framework import serializers
from core.user.models import User
from core.clinic.models import Client
from config import settings
from config.wsgi import *
from core.security.models import *
from django.contrib.auth.models import Permission
from core.clinic.models import *



class HistorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = "__all__"

    def create(self,validated_data):
        sale = Sale(**validated_data)
        sale.save()
        return sale

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields ="__all__"
