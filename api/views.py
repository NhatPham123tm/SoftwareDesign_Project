from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
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
    
    @action(detail=True, methods=['get'])
    def by_id(self, request, pk=None):
        try:
            user = user_accs.objects.get(id=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except user_accs.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=404)

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = permission.objects.all()
    serializer_class = PermissionSerializer
