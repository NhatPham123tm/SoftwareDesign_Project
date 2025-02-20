from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from api.models import user_accs

class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Hashes the password before saving.
    """
    id = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = user_accs
        fields = ["id", "name", "email", "password", "role"]

    def create(self, validated_data):
        validated_data["password_hash"] = make_password(validated_data.pop("password"))  # Hash password
        return user_accs.objects.create(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Validates email and password.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = user_accs.objects.get(email=email)
        except user_accs.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        if not check_password(password, user.password_hash):
            raise serializers.ValidationError("Invalid email or password")

        data["user"] = user
        return data
