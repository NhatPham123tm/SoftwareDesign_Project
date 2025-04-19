from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import user_accs, roles, permission, PayrollAssignment, ReimbursementRequest, ChangeOfAddress, DiplomaRequest, user_ura_accs, work_assign
from .serializers import UserSerializer, RoleSerializer, PermissionSerializer, PayrollAssignmentSerializer, ReimbursementRequestSerializer, ChangeOfAddressSerializer, DiplomaRequestSerializer, UserURASerializer, RequestSerializer, WorkAssignSerializer
import os
import base64
import requests
from .models import Request
from .serializers import RequestSerializer
from django.shortcuts import get_object_or_404
from django_tex.shortcuts import render_to_pdf
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import FileResponse
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from authentication.views import is_admin
from rest_framework.permissions import BasePermission
from django.utils.dateparse import parse_datetime

class RoleViewSet(viewsets.ModelViewSet):
    queryset = roles.objects.all()
    serializer_class = RoleSerializer

class WorkAssignViewSet(viewsets.ModelViewSet):
    queryset = work_assign.objects.all()
    serializer_class = WorkAssignSerializer

    # Read (Retrieve) by ID (GET)
    def retrieve(self, request, *args, **kwargs):
        try:
            user = work_assign.objects.get(id=kwargs['pk'])
            serializer = WorkAssignSerializer(user)
            return Response(serializer.data)
        except work_assign.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    # Update by ID (PUT)
    def update(self, request, *args, **kwargs):
        try:
            user = work_assign.objects.get(id=kwargs['pk'])
            serializer = WorkAssignSerializer(user, data=request.data, partial=False)  # partial=False ensures full update
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except work_assign.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    # Partially Update by ID (PATCH)
    def partial_update(self, request, *args, **kwargs):
        try:
            user = work_assign.objects.get(id=kwargs['pk'])
            serializer = WorkAssignSerializer(user, data=request.data, partial=True) 
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except work_assign.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    # Delete a User by ID (DELETE)
    def destroy(self, request, *args, **kwargs):
        try:
            user = work_assign.objects.get(id=kwargs['pk'])
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except work_assign.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

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
        
class UserURAViewSet(viewsets.ModelViewSet):
    queryset = user_ura_accs.objects.all()
    serializer_class = UserURASerializer

    # Read (Retrieve) by ID (GET)
    def retrieve(self, request, *args, **kwargs):
        try:
            user = user_ura_accs.objects.get(id=kwargs['pk'])
            serializer = UserURASerializer(user)
            return Response(serializer.data)
        except user_ura_accs.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Update by ID (PUT)
    def update(self, request, *args, **kwargs):
        try:
            user = user_ura_accs.objects.get(id=kwargs['pk'])
            serializer = UserURASerializer(user, data=request.data, partial=False)  # partial=False ensures full update
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except user_ura_accs.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    # Partially Update by ID (PATCH)
    def partial_update(self, request, *args, **kwargs):
        try:
            user = user_ura_accs.objects.get(id=kwargs['pk'])
            serializer = UserURASerializer(user, data=request.data, partial=True) 
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except user_ura_accs.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    # Delete a User by ID (DELETE)
    def destroy(self, request, *args, **kwargs):
        try:
            user = user_ura_accs.objects.get(id=kwargs['pk'])
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except user_ura_accs.DoesNotExist:
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

class ChangeOfAddressViewSet(viewsets.ModelViewSet):
    queryset = ChangeOfAddress.objects.all()
    serializer_class = ChangeOfAddressSerializer

    def partial_update(self, request, *args, **kwargs):
        try:
            user = ChangeOfAddress.objects.get(id=kwargs['pk'])
            serializer = ChangeOfAddressSerializer(user, data=request.data, partial=True) 
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ChangeOfAddress.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
    def retrieve(self, request, *args, **kwargs):
        try:
            user = ChangeOfAddress.objects.get(id=kwargs['pk'])
            serializer = ChangeOfAddressSerializer(user)
            return Response(serializer.data)
        except ChangeOfAddress.DoesNotExist:
            return Response({'detail': 'User form not found.'}, status=status.HTTP_404_NOT_FOUND)
        
class DiplomaRequestViewSet(viewsets.ModelViewSet):
    queryset = DiplomaRequest.objects.all()
    serializer_class = DiplomaRequestSerializer

    def partial_update(self, request, *args, **kwargs):
        try:
            user = DiplomaRequest.objects.get(id=kwargs['pk'])
            serializer = DiplomaRequestSerializer(user, data=request.data, partial=True) 
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DiplomaRequest.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
    def retrieve(self, request, *args, **kwargs):
        try:
            user = DiplomaRequest.objects.get(id=kwargs['pk'])
            serializer = DiplomaRequestSerializer(user)
            return Response(serializer.data)
        except DiplomaRequest.DoesNotExist:
            return Response({'detail': 'User form not found.'}, status=status.HTTP_404_NOT_FOUND)

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"detail": "CSRF cookie set"})

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get("name")
        role_id = request.data.get("role", 2)  # default role ID if not provided

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if user_accs.objects.filter(email=email).exists():
                return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

            user = user_accs(
                email=email,
                name=name,
                role_id=role_id
            )
            user.set_password(password)
            user.save()
            return Response({'message': 'Account created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)  # create Django session

            return Response({
                "isSuperUser": user.is_superuser,
                "userId": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role.role_name,
                "status": user.status
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        
class UserFormsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        user_requests = Request.objects.filter(user=user)

        serializer = RequestSerializer(user_requests, many=True)

        return Response(serializer.data)


class RequestSubmitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.data:
            return Response({"error": "No data provided."}, status=status.HTTP_400_BAD_REQUEST)

        form_data = request.data
        form_type = form_data.get("form_type")
        user = request.user
        status_value = form_data.get("status", "draft")
        signature_data = form_data.get('signature')
        signature_file = None
        if signature_data:
            signature_file = self._convert_base64_to_image(signature_data)
        try:
            request_instance = Request.objects.create(
                user=user,
                status=status_value,
                form_type=form_type,
                data=form_data,
                signature=signature_file
            )
            
            return self._process_request(request, request_instance, status_value)
            
        except Exception as e:
            return Response({"error": f"Failed to save the request: {str(e)}"}, 
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk=None):
        if not request.data:
            return Response({"error": "No data provided."}, status=status.HTTP_400_BAD_REQUEST)

        form_data = request.data
        user = request.user
        status_value = form_data.get("status", "draft")
        signature_data = form_data.get('signature')
        signature_file = None
        if signature_data:
            signature_file = self._convert_base64_to_image(signature_data)

        try:
            request_instance = get_object_or_404(Request, id=pk, user=user)
            request_instance.data = form_data
            request_instance.status = status_value


            if signature_file:
                request_instance.signature = signature_file

            request_instance.save()

            return self._process_request(request, request_instance, status_value)
            
        except Exception as e:
            return Response({"error": f"Failed to update the request: {str(e)}"}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def _convert_base64_to_image(self, base64_data):
        try:
            format, imgstr = base64_data.split(';base64,')
            ext = 'jpg' 
            img_data = base64.b64decode(imgstr)


            image_name = f"signature.{ext}"
            image_file = ContentFile(img_data, name=image_name)
            return image_file
        except Exception as e:
            raise ValidationError(f"Invalid signature data: {str(e)}")
        
    
    def _process_request(self, request, request_instance, status_value):
        if status_value == 'submitted' and not request_instance.pdf:
            template_name = "pdf_templates/diploma_template.tex"
            if request_instance.form_type == "ChangeAddressForm":
                template_name = "pdf_templates/change_address_template.tex"
            context = request_instance.data
            
            try:
                pdf_path = self.generate_pdf(request, template_name, context, request_instance)
                if not pdf_path:
                    return Response({"error": "Failed to generate PDF"}, 
                                   status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({"error": f"PDF generation failed: {str(e)}"}, 
                               status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        serializer = RequestSerializer(request_instance)
        return Response({
            "message": "Request saved successfully.",
            "request": serializer.data
        })

    def generate_pdf(self, request, template_name, context, request_instance):
        def flatten_dict(d):
            flat = {}
            for key, value in d.items():
                if isinstance(value, dict):
                    flat.update(flatten_dict(value))
                else:
                    flat[key] = value
            return flat

        context = flatten_dict(context)

        context['graphicspath'] = os.path.join(settings.MEDIA_ROOT, 'signatures').replace("\\", "/")


        if request_instance.signature:
            context['signature'] = request_instance.signature.path.replace("\\", "/")
        else:
            context['signature'] = None
            
        form_type = request_instance.form_type
        pdf_file_name = f'{form_type}_{request_instance.id}.pdf'

        pdf_path = os.path.join(f'{form_type}_pdfs', pdf_file_name)
        full_path = os.path.join(settings.MEDIA_ROOT, pdf_path)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        try:
            rendered_pdf = render_to_pdf(request, template_name, context)
            
            if rendered_pdf is None:
                raise ValueError("PDF rendering returned None")
            
            with open(full_path, 'wb') as f:
                f.write(rendered_pdf.content)

            request_instance.pdf.name = pdf_path
            request_instance.save()

            return full_path
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error generating PDF: {e}", exc_info=True)
            return None
    
def servePDF(request, request_id):
    req = get_object_or_404(Request, id=request_id)

    if req.pdf:
        return FileResponse(req.pdf, content_type='application/pdf')
    else:
        return HttpResponse('PDF not found', status=404)
    
class RequestDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        user_request = get_object_or_404(Request, id=pk, user=request.user)
        
        user_request.delete()

        return Response({"message": "Form deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class IsAdminUserRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role_id', None) == 1
    
class AdminRequestsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserRole]
    def get(self, request):
        submitted_requests = Request.objects.exclude(status='Draft')
        serializer = RequestSerializer(submitted_requests, many=True)
        return Response(serializer.data)

class RequestApprovalView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserRole]
    def put(self, request, pk):
        req = get_object_or_404(Request, id=pk)
        new_status = request.data.get("status")
        if new_status not in ['approved', 'rejected']:
            return Response(
                {"error": "Invalid status. Must be 'approved' or 'rejected'."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if new_status == "rejected":
            reason = request.data.get("reason_for_return", "")
            req.reason_for_return = reason
        else:
            req.reason_for_return = None


        admin_signature_data = request.data.get('admin_signature')
        admin_signature_file = None

        if admin_signature_data:
            admin_signature_file = self._convert_base64_to_image(admin_signature_data)

        if admin_signature_file:
            try:
                req.admin_signature = admin_signature_file
                req.status = new_status 
                req.save()

                return self._process_request(request, req, new_status)
            except Exception as e:
                return Response({"error": f"Failed to save the admin signature: {str(e)}"}, 
                                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        req.status = new_status
        req.save()

        return Response(
            {"message": f"Request {new_status} successfully."},
            status=status.HTTP_200_OK,
        )
    # * -------------- Everything below this needs to be refactored somehow -------------- *
    # Redundant code used in RequestSubmitView
    def _convert_base64_to_image(self, base64_data):
        try:
            format, imgstr = base64_data.split(';base64,')
            ext = 'jpg' 
            img_data = base64.b64decode(imgstr)

            image_name = f"admin_signature.{ext}"
            image_file = ContentFile(img_data, name=image_name)
            return image_file
        except Exception as e:
            raise ValidationError(f"Invalid signature data: {str(e)}")

    def _process_request(self, request, request_instance, status_value):
        if status_value == 'approved':
            template_name = "pdf_templates/diploma_template_admin.tex"
            if request_instance.form_type == "ChangeAddressForm":
                template_name = "pdf_templates/change_address_template_admin.tex"
            context = request_instance.data

            try:
                pdf_path = self.generate_pdf(request, template_name, context, request_instance)
                if not pdf_path:
                    return Response({"error": "Failed to generate PDF"}, 
                                     status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({"error": f"PDF generation failed: {str(e)}"}, 
                                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        serializer = RequestSerializer(request_instance)
        return Response({
            "message": "Request saved successfully.",
            "request": serializer.data
        })

    def generate_pdf(self, request, template_name, context, request_instance):
        def flatten_dict(d):
            flat = {}
            for key, value in d.items():
                if isinstance(value, dict):
                    flat.update(flatten_dict(value))
                else:
                    flat[key] = value
            return flat

        context = flatten_dict(context)

        context['graphicspath'] = os.path.join(settings.MEDIA_ROOT, 'signatures').replace("\\", "/")
        context['signature'] = request_instance.signature.path.replace("\\", "/") if request_instance.signature else None
        context['admin_signature'] = request_instance.admin_signature.path.replace("\\", "/") if request_instance.admin_signature else None

        form_type = request_instance.form_type
        pdf_file_name = f'{form_type}_{request_instance.id}.pdf'

        pdf_path = os.path.join(f'{form_type}_pdfs', pdf_file_name)
        full_path = os.path.join(settings.MEDIA_ROOT, pdf_path)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        try:
            rendered_pdf = render_to_pdf(request, template_name, context)

            if rendered_pdf is None:
                raise ValueError("PDF rendering returned None")

            with open(full_path, 'wb') as f:
                f.write(rendered_pdf.content)

            request_instance.pdf.name = pdf_path
            request_instance.save()

            return full_path

        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error generating PDF: {e}", exc_info=True)
            return None
        
def create_work_assignment(request):
    if request.method == 'POST':
        assignee_id = request.POST.get('assignee')
        form_type = request.POST.get('form_type')
        form_id = request.POST.get('form_id')
        due_date_str = request.POST.get('due_date')

        assignee = get_object_or_404(user_accs, id=assignee_id)
        due_date = parse_datetime(due_date_str) if due_date_str else None

        assignment = work_assign(
            user=assignee,
            created_by=request.user,
            deadline=due_date,
            status='Pending'
        )

        if form_type == 'payroll':
            assignment.PayrollAssignment_id = get_object_or_404(PayrollAssignment, id=form_id)
        elif form_type == 'reimburse':
            assignment.ReimbursementRequest_id = get_object_or_404(ReimbursementRequest, id=form_id)
        elif form_type == 'address':
            assignment.ChangeOfAddress_id = get_object_or_404(ChangeOfAddress, id=form_id)
        elif form_type == 'diploma':
            assignment.DiplomaRequest_id = get_object_or_404(DiplomaRequest, id=form_id)
        else:
            return JsonResponse({'error': 'Invalid form type'}, status=400)

        try:
            assignment.save()
            return JsonResponse({'message': 'Work assigned successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)