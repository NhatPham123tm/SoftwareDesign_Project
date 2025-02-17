from rest_framework import viewsets
from .models import user_accs, roles, address, permission
from .serializers import UserSerializer, RoleSerializer, AddressSerializer, PermissionSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = roles.objects.all()
    serializer_class = RoleSerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = address.objects.all()
    serializer_class = AddressSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = user_accs.objects.all()
    serializer_class = UserSerializer

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = permission.objects.all()
    serializer_class = PermissionSerializer
