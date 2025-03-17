from django.urls import path, include
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RoleViewSet, PermissionViewSet, PayrollAssignmentViewSet

# Use DRF Router to auto-generate URLs
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'payroll', PayrollAssignmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]