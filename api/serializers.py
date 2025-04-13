from rest_framework import serializers
from .models import user_accs, roles, permission, PayrollAssignment, ReimbursementRequest, Request, ChangeOfAddress, DiplomaRequest

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = roles
        fields = '__all__'  # Serialize all fields


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)  # Nested serializer to show role details
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=roles.objects.all(), source='role', write_only=True
    )  # Allow assigning role by ID


    class Meta:
        model = user_accs
        fields = ['id', 'name', 'email', 'password_hash', 'role', 'role_id', 'phone_number', 
                  'address', 'address', 'status', 'created_at']
        extra_kwargs = {'password_hash': {'write_only': True}}  # Hide password in responses

    def create(self, validated_data):
        """Hash password before saving"""
        validated_data['password_hash'] = serializers.HiddenField(default='')
        return super().create(validated_data)

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = permission
        fields = '__all__'

class PayrollAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollAssignment
        fields = '__all__'

class ReimbursementRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReimbursementRequest
        fields = '__all__'

class RequestSerializer(serializers.ModelSerializer):
    signature = serializers.ImageField(required=False, allow_null = True)
    admin_signature = serializers.ImageField(required=False, allow_null = True)

    class Meta:
        model = Request
        fields = ['id', 'status', 'reason_for_return', 'form_type','data', 'pdf', 'signature', 'admin_signature']
        read_only_fields = ['id']

class ChangeOfAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeOfAddress
        fields = '__all__'
 