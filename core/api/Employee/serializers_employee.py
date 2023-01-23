from rest_framework import serializers
from core.user.models import User
from core.clinic.models import Client
from config import settings
from config.wsgi import *
from core.security.models import *
from django.contrib.auth.models import Permission
from core.clinic.models import *

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields ="__all__"
    def to_representation(self,instance):
        return {
            'id' : instance.id,
            'full_name' : instance.user.get_full_name() if instance.user is not None else "",
        }