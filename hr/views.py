from rest_framework import generics, viewsets, permissions
from hr.models import Employee, EmployeeOffice, EmployeeTitle, Office, Title
from hr.serializers import EmployeeOfficeSerializer, EmployeeSerializer, EmployeeTitleSerializer, OfficeSerializer, TitleSerializer



# Create your views here.
class OfficeViewSet(viewsets.ModelViewSet):
    queryset  = Office.objects.all()
    serializer_class = OfficeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TitleViewSet(viewsets.ModelViewSet):
    queryset  = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset  = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
                          

class EmployeeTitleViewSet(viewsets.ModelViewSet):
    queryset  = EmployeeTitle.objects.all()
    serializer_class = EmployeeTitleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

  
class EmployeeOfficeViewSet(viewsets.ModelViewSet):
    queryset  = EmployeeOffice.objects.all()
    serializer_class = EmployeeOfficeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

