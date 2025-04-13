from django.urls import path, include
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RoleViewSet, PermissionViewSet, PayrollAssignmentViewSet, ReimbursementRequestViewSet, ChangeOfAddressViewSet
from .views import RequestSubmitView, SignupView, LoginView, UserFormsView, servePDF, RequestDeleteView, AdminRequestsView, RequestApprovalView
from authentication import views

# Use DRF Router to auto-generate URLs
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'payroll', PayrollAssignmentViewSet)
router.register(r'reimburse', ReimbursementRequestViewSet)
router.register(r'address', ChangeOfAddressViewSet)


urlpatterns = [
    path('users/forms/', UserFormsView.as_view(), name='user-forms'),
    path('', include(router.urls)),
    # Users can view these
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin/requests/', AdminRequestsView.as_view(), name='admin-requests'),
    path('auth/', include('allauth.urls')),
    path("login/microsoft/", views.microsoft_login_json, name="microsoft_login"),
    path("login/microsoft/callback/", views.microsoft_callback, name="microsoft_callback"),
    path("auth/data/", views.get_auth_data, name="auth_data"),
    # For managing forms
    path('forms/', RequestSubmitView.as_view(), name='form'),
    path('forms/<int:pk>/', RequestSubmitView.as_view(), name='form'),
    path('forms/<int:request_id>/pdf/', servePDF, name='serve_pdf'),
    path('forms/<int:pk>/delete/', RequestDeleteView.as_view(), name='delete_form'),
    path('admin/requests/<int:pk>/approved/', RequestApprovalView.as_view(), name='admin-approve-request'),
    path('admin/requests/<int:pk>/rejected/', RequestApprovalView.as_view(), name='admin-reject-request'),
]
