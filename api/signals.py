from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from api.models import roles, user_accs, permission, user_ura_accs, work_assign, PayrollAssignment, ReimbursementRequest, ChangeOfAddress, DiplomaRequest, Workflow, WorkflowStep, ManagerNotification

@receiver(post_save, sender=work_assign)
def handle_work_assign_status(sender, instance, created, **kwargs):
    # Step 1: ensure is_current_step = False if status is Completed
    if instance.status == "Completed" and instance.is_current_step:
        instance.is_current_step = False
        instance.save(update_fields=["is_current_step"])

    # Step 2: recursively complete all delegated-to tasks
    def mark_chain(assign):
        delegated = assign.delegated
        if delegated and (delegated.status != "Completed" or delegated.is_current_step):
            delegated.status = "Completed"
            delegated.is_current_step = False
            delegated.save()
            mark_chain(delegated)

    if instance.status == "Completed" and not instance.is_current_step:
        mark_chain(instance)

    if not created and instance.delegated and instance.status in ["Completed", "Rejected"]:
        assigner = instance.created_by
        actor = instance.user
        message = f"Assigned Work (ID #{instance.id}) was reviewed."

        ManagerNotification.objects.create(
            recipient=assigner,
            message=message
        )
        
        ManagerNotification.objects.create(
            recipient=actor,
            message=message
        )
    

@receiver(post_save, sender=work_assign)
def handle_work_assign_status2(sender, instance, created, **kwargs):
    # Step 1: Ensure is_current_step is False if Completed
    if instance.status == "Completed" and instance.is_current_step:
        instance.is_current_step = False
        instance.save(update_fields=["is_current_step"])

    # Step 2: Recursively complete all tasks that delegated FROM this one
    def mark_delegated_chain(assign):
        for child in assign.delegated_tasks.all():  # delegated FROM this assign
            if child.status != "Completed" or child.is_current_step:
                child.status = "Completed"
                child.is_current_step = False
                child.save()
                mark_delegated_chain(child)

    # If already completed and not current, check for delegated chain
    if instance.status == "Completed" and not instance.is_current_step:
        mark_delegated_chain(instance)


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
    # Check if a workflow with this form_type already exists
        existing_workflow = Workflow.objects.filter(form_type=wf["form_type"]).first()
        
        if existing_workflow:
            workflow = existing_workflow
            print(f"Workflow already exists for {wf['form_type']}: {workflow.name}")
        else:
            workflow = Workflow.objects.create(
                name=wf["workflow_name"],
                form_type=wf["form_type"]
            )
            print(f"Created workflow: {workflow.name}")

        # Only add a step if none exists yet
        if not WorkflowStep.objects.filter(workflow=workflow).exists():
            WorkflowStep.objects.create(
                workflow=workflow,
                step_order=1,
                label=wf["label"],
                role=wf["role"],
                department=wf["department"]
            )
            print(f"Created step for {wf['form_type']} → {wf['role'].role_name}")

    workflow, created = Workflow.objects.get_or_create(
        name="Uranium's Request Workflow",
        form_type="Request"
    )
    if created:
        print("Created default workflow for Uranium Request")

    # Create default step for the Request workflow
    if not WorkflowStep.objects.filter(workflow=workflow).exists():
        WorkflowStep.objects.create(
            workflow=workflow,
            step_order=1,
            label="Initial Request Review",
            role=admin_role,
            department="all"
        )
        print("Created default step for Request assigned to admin")