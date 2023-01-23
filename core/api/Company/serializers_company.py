from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.homepage.models import *
from core.user.models import User

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Mainpage
        fields = "__all__"

