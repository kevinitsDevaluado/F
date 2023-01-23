from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from core.user.models import User
from core.clinic.models import *
from core.homepage.models import *
from core.api.User.serializers_user import UserSerializer,UserTokenSerializerJWT,CustomUserSerializer
from core.api.Company.serializers_company import *
class CompanyViewSet(viewsets.GenericViewSet):
    model = Mainpage
    serializer_class = CompanySerializer

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.all()
        return self.queryset
    
    def list(self,request):
        user = self.get_queryset()
        if user:
            company_serializer = self.serializer_class(user,many=True)
            return Response(company_serializer.data, status = status.HTTP_200_OK)
        return Response({"message":"No hay ninguna usuario"}, status = status.HTTP_400_BAD_REQUEST)


