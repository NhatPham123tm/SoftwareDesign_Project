from django.urls import path, include
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RoleViewSet, PermissionViewSet, PayrollAssignmentViewSet, ReimbursementRequestViewSet

# Use DRF Router to auto-generate URLs
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'payroll', PayrollAssignmentViewSet)
router.register(r'reimburse', ReimbursementRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
