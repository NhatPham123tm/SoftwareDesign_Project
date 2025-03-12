from django.urls import path, include
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RoleViewSet, PermissionViewSet, PayrollAssignmentViewSet, PositionInformationViewSet

# Use DRF Router to auto-generate URLs
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'payroll', PayrollAssignmentViewSet)
payroll_router = routers.NestedDefaultRouter(router, r'payroll', lookup='payroll_assignment')
payroll_router.register(r'positions', PositionInformationViewSet, basename='payroll-positions')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(payroll_router.urls)), 
]