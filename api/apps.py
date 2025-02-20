from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError, IntegrityError
from django.contrib.auth.hashers import make_password
from django.db import connection

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from django.db import connection

        # Ensure tables exist before querying
        if not self.check_db_ready():
            return

        from api.models import roles, user_accs, permission

        try:
            # Ensure roles exist
            admin_role, _ = roles.objects.get_or_create(role_name="admin")
            basic_user_role, _ = roles.objects.get_or_create(role_name="basicuser")

            # Ensure some users exist
            user_data = [
                {
                    "name": "Admin User",
                    "email": "admin@example.com",
                    "password": "admin123",
                    "role": admin_role,
                    "phone_number": "1234567890",
                    "address": "123 Admin Street",
                    "status": "active",
                    "is_staff": True,
                    "is_superuser": True,
                },
                {
                    "name": "Basic User",
                    "email": "user@example.com",
                    "password": "user123",
                    "role": basic_user_role,
                    "phone_number": "9876543210",
                    "address": "456 User Lane",
                    "status": "active",
                    "is_staff": False,
                    "is_superuser": False,
                },
            ]

            for user_info in user_data:
                if not user_accs.objects.filter(email=user_info["email"]).exists():
                    user_accs.objects.create(
                        name=user_info["name"],
                        email=user_info["email"],
                        password_hash=make_password(user_info["password"]),
                        role=user_info["role"],
                        phone_number=user_info["phone_number"],
                        address=user_info["address"],
                        status=user_info["status"],
                        is_staff=user_info["is_staff"],
                        is_superuser=user_info["is_superuser"],
                    )

            # Initialize permissions for each role
            permission_data = [
                ("admin", "Can manage users"),
                ("admin", "Can view reports"),
                ("admin", "Can delete content"),
                ("basicuser", "Can edit profile"),
                ("basicuser", "Can post comments"),
            ]

            for role_name, permission_detail in permission_data:
                role = roles.objects.get(role_name=role_name)
                permission.objects.get_or_create(role=role, permission_detail=permission_detail)

        except (OperationalError, IntegrityError, ProgrammingError):
            # Database is not ready yet, so skip initialization
            pass

    def check_db_ready(self):
        """Check if database tables exist before running queries."""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM api_roles LIMIT 1;")
            return True
        except ProgrammingError:
            return False
