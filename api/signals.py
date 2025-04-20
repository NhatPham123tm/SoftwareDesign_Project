from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from api.models import roles, user_accs, permission, user_ura_accs, work_assign, PayrollAssignment, ReimbursementRequest, ChangeOfAddress, DiplomaRequest

@receiver(post_migrate)
def initialize_data(sender, **kwargs):
    """Initialize default roles, users, and permissions after migrations."""
    if sender.name != "api":  # Ensure it only runs for this app
        return

    # Ensure roles exist
    admin_role, _ = roles.objects.get_or_create(role_name="admin", level=1, department="all")
    basic_user_role, _ = roles.objects.get_or_create(role_name="basicuser", level=99, department="all")
    manager_role_finance, _ = roles.objects.get_or_create(role_name="manager", level=2, department="finance")
    manager_role_registrar, _ = roles.objects.get_or_create(role_name="manager", level=2, department="registrar")
    employee_role_finance, _ = roles.objects.get_or_create(role_name="employee", level=3, department="finance")
    employee_role_registrar, _ = roles.objects.get_or_create(role_name="employee", level=3, department="registrar")

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
        {
            "name": "Finance Manager",
            "email": "finmanager@example.com",
            "password": "manager123",
            "role": manager_role_finance,
            "phone_number": "1112223333",
            "address": "789 Finance Blvd",
            "status": "active",
            "is_staff": False,
            "is_superuser": False,
        },
        {
            "name": "Registrar Manager",
            "email": "regmanager@example.com",
            "password": "manager123",
            "role": manager_role_registrar,
            "phone_number": "4445556666",
            "address": "321 Registrar Rd",
            "status": "active",
            "is_staff": False,
            "is_superuser": False,
        },
        {
            "name": "Finance Employee",
            "email": "finemployee@example.com",
            "password": "employee123",
            "role": employee_role_finance,
            "phone_number": "7778889999",
            "address": "654 Finance St",
            "status": "active",
            "is_staff": False,
            "is_superuser": False,
        },
        {
            "name": "Registrar Employee",
            "email": "regemployee@example.com",
            "password": "employee123",
            "role": employee_role_registrar,
            "phone_number": "0001112222",
            "address": "987 Registrar Ave",
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

    for user_info in user_data:
        if not user_ura_accs.objects.filter(email=user_info["email"]).exists():
            user_ura_accs.objects.create(
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

    default_workflows = [
        {
            "form_type": "PayrollAssignment",
            "workflow_name": "Payroll Workflow",
            "label": "Initial Payroll Approval",
            "role": manager_role_finance,
            "department": "finance",
        },
        {
            "form_type": "ReimbursementRequest",
            "workflow_name": "Reimbursement Workflow",
            "label": "Initial Reimbursement Approval",
            "role": manager_role_finance,
            "department": "finance",
        },
        {
            "form_type": "ChangeOfAddress",
            "workflow_name": "Address Change Workflow",
            "label": "Initial Address Approval",
            "role": manager_role_registrar,
            "department": "registrar",
        },
        {
            "form_type": "DiplomaRequest",
            "workflow_name": "Diploma Approval Workflow",
            "label": "Initial Diploma Approval",
            "role": manager_role_registrar,
            "department": "registrar",
        },
    ]

    for wf in default_workflows:
        workflow, created = Workflow.objects.get_or_create(
            name=wf["workflow_name"],
            form_type=wf["form_type"]
        )
        if created:
            print("Created workflow:", wf["workflow_name"])

        if not WorkflowStep.objects.filter(workflow=workflow).exists():
            WorkflowStep.objects.create(
                workflow=workflow,
                step_order=1,
                label=wf["label"],
                role=wf["role"],
                department=wf["department"]
            )
            