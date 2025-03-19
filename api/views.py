from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import user_accs, roles, permission, PayrollAssignment, ReimbursementRequest
from .serializers import UserSerializer, RoleSerializer, PermissionSerializer, PayrollAssignmentSerializer, ReimbursementRequestSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = roles.objects.all()
    serializer_class = RoleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = user_accs.objects.all()
    serializer_class = UserSerializer

    # Read (Retrieve) by ID (GET)
    def retrieve(self, request, *args, **kwargs):
        try:
            user = user_accs.objects.get(id=kwargs['pk'])
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except user_accs.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Update by ID (PUT)
    def update(self, request, *args, **kwargs):
        try:
            user = user_accs.objects.get(id=kwargs['pk'])
            serializer = UserSerializer(user, data=request.data, partial=False)  # partial=False ensures full update
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except user_accs.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Partially Update by ID (PATCH)
    def partial_update(self, request, *args, **kwargs):
        try:
            user = user_accs.objects.get(id=kwargs['pk'])
            serializer = UserSerializer(user, data=request.data, partial=True) 
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except user_accs.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Delete a User by ID (DELETE)
    def destroy(self, request, *args, **kwargs):
        try:
            user = user_accs.objects.get(id=kwargs['pk'])
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except user_accs.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
class PermissionViewSet(viewsets.ModelViewSet):
    queryset = permission.objects.all()
    serializer_class = PermissionSerializer

class PayrollAssignmentViewSet(viewsets.ModelViewSet):
    queryset = PayrollAssignment.objects.all()
    serializer_class = PayrollAssignmentSerializer
    def partial_update(self, request, *args, **kwargs):
        try:
            user = PayrollAssignment.objects.get(id=kwargs['pk'])
            serializer = PayrollAssignmentSerializer(user, data=request.data, partial=True) 
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PayrollAssignment.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
    def retrieve(self, request, *args, **kwargs):
        try:
            user = PayrollAssignment.objects.get(id=kwargs['pk'])
            serializer = PayrollAssignmentSerializer(user)
            return Response(serializer.data)
        except PayrollAssignment.DoesNotExist:
            return Response({'detail': 'User form not found.'}, status=status.HTTP_404_NOT_FOUND)

class ReimbursementRequestViewSet(viewsets.ModelViewSet):
    queryset = ReimbursementRequest.objects.all()
    serializer_class = ReimbursementRequestSerializer

    def partial_update(self, request, *args, **kwargs):
        try:
            user = ReimbursementRequest.objects.get(id=kwargs['pk'])
            serializer = ReimbursementRequestSerializer(user, data=request.data, partial=True) 
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ReimbursementRequest.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
    def retrieve(self, request, *args, **kwargs):
        try:
            user = ReimbursementRequest.objects.get(id=kwargs['pk'])
            serializer = ReimbursementRequestSerializer(user)
            return Response(serializer.data)
        except ReimbursementRequest.DoesNotExist:
            return Response({'detail': 'User form not found.'}, status=status.HTTP_404_NOT_FOUND)
