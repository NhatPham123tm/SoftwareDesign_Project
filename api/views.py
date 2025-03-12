from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import user_accs, roles, permission, PayrollAssignment, PositionInformation
from .serializers import UserSerializer, RoleSerializer, PermissionSerializer, PayrollAssignmentSerializer, PositionInformationSerializer

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

class PositionInformationViewSet(viewsets.ModelViewSet):
    serializer_class = PositionInformationSerializer

    def get_queryset(self):
        """
        Filters PositionInformation records based on the PayrollAssignment ID.
        """
        payroll_assignment_id = self.kwargs.get('payroll_assignment_pk')
        return PositionInformation.objects.filter(payroll_assignment_id=payroll_assignment_id)
