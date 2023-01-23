from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.api.User.views_user import UserViewSet, Login, Logout
from core.api.User.views_getUser import *
from core.api.Client.views_client import ClientViewSet
from core.api.Client.views_getClient import *
from core.api.Company.views_company import *
from core.api.HistorialMedical.views_company import *
from core.api.Mascots.views_mascots import *
from core.api.Employee.views_getEmployee import *
router = DefaultRouter()

router.register(r'UsersApi', UserViewSet, basename='UsersApi')
router.register(r'Client', ClientViewSet, basename='Client')
router.register(r'GetClient', ClientGetViewSet, basename='GetClient')
router.register(r'GetProfile', UserGetViewSet, basename='GetProfile')
router.register(r'Company', CompanyViewSet, basename='Company')
router.register(r'Historial', HistorialViewSet, basename='Historial')
router.register(r'Mascots', MascotsViewSet, basename='Mascots')
router.register(r'Employee', EmployeeViewSet, basename='Employee')


urlpatterns = [
    path('', include(router.urls), name="ViewApi"),
    path('Login/', Login.as_view(), name="Login"),
    path('Logout/', Logout.as_view(), name="Logout"),
]