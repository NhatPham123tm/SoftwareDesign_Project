from api.models import Workflow, WorkflowStep, work_assign, PayrollAssignment, user_accs
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from api.models import Workflow, WorkflowStep, roles, user_accs
from django.contrib import messages
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from api.models import Workflow, WorkflowStep, roles, user_accs
from django.shortcuts import get_object_or_404

def assign_workflow_steps(form_instance):
    form_type = form_instance.__class__.__name__
    user = form_instance.user

    # Get the workflow matching this form type
    try:
        workflow = Workflow.objects.get(form_type=form_type)
    except Workflow.DoesNotExist:
        return  # or raise an error

    steps = workflow.steps.all().order_by("step_order")

    for i, step in enumerate(steps):
        is_current = (i == 0)  # Only the first step is current at the beginning

        if step.user:
            # Direct assignment to a specific user
            work_assign.objects.create(
                user=step.user,
                created_by=user,
                PayrollAssignment_id=form_instance if form_type == "PayrollAssignment" else None,
                ReimbursementRequest_id=form_instance if form_type == "ReimbursementRequest" else None,
                ChangeOfAddress_id=form_instance if form_type == "ChangeOfAddress" else None,
                DiplomaRequest_id=form_instance if form_type == "DiplomaRequest" else None,
                step=step,
                is_current_step=is_current
            )
        
        elif step.role:
            users = form_instance.__class__.user.field.related_model.objects.filter(role=step.role)

            if step.department and step.department != 'all':
                users = users.filter(role__department=step.department)

            for i in users:
                work_assign.objects.create(
                    user=i,
                    created_by=user,
                    PayrollAssignment_id=form_instance if form_type == "PayrollAssignment" else None,
                    ReimbursementRequest_id=form_instance if form_type == "ReimbursementRequest" else None,
                    ChangeOfAddress_id=form_instance if form_type == "ChangeOfAddress" else None,
                    DiplomaRequest_id=form_instance if form_type == "DiplomaRequest" else None,
                    step=step,
                    is_current_step=is_current
                )

def advance_to_next_workflow_step(form_instance):
    form_type = form_instance.__class__.__name__

    current_assignments = work_assign.objects.filter(
        is_current_step=True,
        PayrollAssignment_id=form_instance if form_type == "PayrollAssignment" else None,
        ReimbursementRequest_id=form_instance if form_type == "ReimbursementRequest" else None,
        ChangeOfAddress_id=form_instance if form_type == "ChangeOfAddress" else None,
        DiplomaRequest_id=form_instance if form_type == "DiplomaRequest" else None,
    )

    if not current_assignments.exists():
        return

    current_step_order = current_assignments.first().step.step_order
    workflow = current_assignments.first().step.workflow

    # Complete current step
    current_assignments.update(is_current_step=False, status="Completed")

    # Get next step
    next_step = WorkflowStep.objects.filter(workflow=workflow, step_order=current_step_order + 1).first()
    if next_step:
        assign_workflow_steps_for_step(form_instance, next_step)

def assign_workflow_steps_for_step(form_instance, step):
    form_type = form_instance.__class__.__name__

    if step.user:
        work_assign.objects.create(
            user=step.user,
            created_by=form_instance.user,
            step=step,
            is_current_step=True,
            PayrollAssignment_id=form_instance if form_type == "PayrollAssignment" else None,
            ReimbursementRequest_id=form_instance if form_type == "ReimbursementRequest" else None,
            ChangeOfAddress_id=form_instance if form_type == "ChangeOfAddress" else None,
            DiplomaRequest_id=form_instance if form_type == "DiplomaRequest" else None,
        )
    elif step.role:
        users = user_accs.objects.filter(role=step.role)
        if step.department and step.department != 'all':
            users = users.filter(role__department=step.department)
        for user in users:
            work_assign.objects.create(
                user=user,
                created_by=form_instance.user,
                step=step,
                is_current_step=True,
                PayrollAssignment_id=form_instance if form_type == "PayrollAssignment" else None,
                ReimbursementRequest_id=form_instance if form_type == "ReimbursementRequest" else None,
                ChangeOfAddress_id=form_instance if form_type == "ChangeOfAddress" else None,
                DiplomaRequest_id=form_instance if form_type == "DiplomaRequest" else None,
            )


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def workflow_list_create(request):
    if request.user.role.level != 1:
        return Response({"detail": "Access denied"}, status=403)

    if request.method == "GET":
        workflows = Workflow.objects.all().values("id", "name", "form_type")
        return Response(list(workflows))

    if request.method == "POST":
        name = request.data.get("name")
        form_type = request.data.get("form_type")
        if not name or not form_type:
            return Response({"error": "Missing fields"}, status=400)
        workflow = Workflow.objects.create(name=name, form_type=form_type)
        return Response({"id": workflow.id, "name": workflow.name}, status=201)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def workflow_steps(request, workflow_id):
    if request.user.role.level != 1:
        return Response({"detail": "Access denied"}, status=403)

    workflow = get_object_or_404(Workflow, id=workflow_id)

    if request.method == "GET":
        steps = WorkflowStep.objects.filter(workflow=workflow).order_by("step_order")
        data = []
        for step in steps:
            data.append({
                "id": step.id,
                "step_order": step.step_order,
                "label": step.label,
                "role_id": step.role.id if step.role else None,
                "role_name": step.role.role_name if step.role else None,
                "user_id": step.user.id if step.user else None,
                "user_name": step.user.name if step.user else None,
                "department": step.department,
            })
        return Response(data)

    if request.method == "POST":
        step_order = request.data.get("step_order")
        label = request.data.get("label")
        role_id = request.data.get("role_id")
        user_id = request.data.get("user_id")
        department = request.data.get("department")

        if not step_order or not label:
            return Response({"error": "Missing step_order or label"}, status=400)

        if not role_id and not user_id:
            return Response({"error": "Either role_id or user_id is required."}, status=400)

        if role_id and user_id:
            return Response({"error": "Only one of role_id or user_id should be set."}, status=400)

        step = WorkflowStep(
            workflow=workflow,
            step_order=step_order,
            label=label,
            department=department
        )

        if role_id:
            step.role = get_object_or_404(roles, id=role_id)
        if user_id:
            step.user = get_object_or_404(user_accs, id=user_id)

        step.save()
        return Response({"message": "Step created."}, status=201)
    
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_workflow(request, workflow_id):
    if request.user.role.level != 1:
        return Response({"detail": "Access denied"}, status=403)

    workflow = get_object_or_404(Workflow, id=workflow_id)
    workflow.delete()
    return Response({"message": "Workflow deleted."}, status=200)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_workflow_step(request, step_id):
    if request.user.role.level != 1:
        return Response({"detail": "Access denied"}, status=403)

    step = get_object_or_404(WorkflowStep, id=step_id)
    step.delete()
    return Response({"message": "Step deleted."}, status=200)