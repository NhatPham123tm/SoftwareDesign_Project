from django.contrib import admin
from django.urls import path, include
from authentication.views import home  # Import the home view
from authentication.views import microsoft_callback, dashboard, user_login, register_page ,microsoft_login,microsoft_logout, login_page, user_register, basicuser, adminpage, get_userLoad, reset_password,suspend, get_auth_data, forms, check_id_exists, check_email_exists, landing
from authentication import views
from django.contrib.auth import views as auth_views
from formProcessor.views import reimbursement_step1, reimbursement_step2, reimbursement_step3, generate_reimbursement_pdf, delete_reimbursement, view_pdf, generate_payroll_pdf, view_pdf2, view_payroll_pdf2, view_pdf3, view_payroll_pdf3, change_address_step1, change_address_step2, change_address_step3, diploma_step1, diploma_step2, delete_address, delete_diploma, generate_change_address_pdf, generate_diploma_pdf
from formProcessor.views import (
    payroll_step1, payroll_step2, payroll_step3, payroll_step4,
    payroll_step5, payroll_step6, payroll_step7, payroll_step8,
    payroll_step9, payroll_step10, payroll_review, delete_payroll, view_payroll_pdf,
    view_change_address_pdf, view_diploma_pdf, view_change_address_pdf3, view_diploma_pdf3
)
from api.views import get_csrf_token
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trois-rivieres/', home, name='home'),  # Define the root URL
    path('', landing, name='landing'),
    path('auth/complete/azure/', microsoft_callback, name='microsoft-callback'),
    path('dashboard/', dashboard, name='dashboard'),
    path('api/', include('api.urls')),
    path("register/", register_page, name="register_page"),
    path("api/user_register/", user_register, name="register"),
    path('login/microsoft/', microsoft_login, name='microsoft-login'),
    path("api/user_login/", user_login, name="api_login"),
    path('logout/', microsoft_logout, name='microsoft-logout'),
    path("login/", login_page, name="login_page"),  # Renders login.html
    path('basicuser/', basicuser, name='basicuser'),
    path('home/', home, name='home'),
    path('reset_password/', reset_password, name='reset_password'),
    path('adminpage/', adminpage, name='adminpage'),
    path('api/get_userLoad/', get_userLoad, name='get_userLoad'),
    path('suspend/', suspend, name='suspend'),
    path("api/microsoft-login/", get_auth_data, name="microsoft-login-json"),
    # for testing
    path('generate_payroll_pdf/', generate_payroll_pdf, name='generate_payroll_pdf'),
    # still developing
    path('reimbursement/step1/', reimbursement_step1, name='reimbursement_step1'),
    path('reimbursement/step2/<int:reimbursement_id>/', reimbursement_step2, name='reimbursement_step2'),
    path('reimbursement/step3/<int:reimbursement_id>/', reimbursement_step3, name='reimbursement_step3'),
    path('generate_reimbursement_pdf/<int:reimbursement_id>/', generate_reimbursement_pdf, name='generate_reimbursement_pdf'),
    path('reimbursement/delete/<int:reimbursement_id>/', delete_reimbursement, name='delete_reimbursement'),
    path('view_pdf/', view_pdf, name='view_pdf'),
    # payroll
    path('payroll/step1/', payroll_step1, name='payroll_step1'),
    path('payroll/step2/<int:payroll_id>/', payroll_step2, name='payroll_step2'),
    path('payroll/step3/<int:payroll_id>/', payroll_step3, name='payroll_step3'),
    path('payroll/step4/<int:payroll_id>/', payroll_step4, name='payroll_step4'),
    path('payroll/step5/<int:payroll_id>/', payroll_step5, name='payroll_step5'),
    path('payroll/step6/<int:payroll_id>/', payroll_step6, name='payroll_step6'),
    path('payroll/step7/<int:payroll_id>/', payroll_step7, name='payroll_step7'),
    path('payroll/step8/<int:payroll_id>/', payroll_step8, name='payroll_step8'),
    path('payroll/step9/<int:payroll_id>/', payroll_step9, name='payroll_step9'),
    path('payroll/step10/<int:payroll_id>/', payroll_step10, name='payroll_step10'),
    path('payroll/review/<int:payroll_id>/', payroll_review, name='payroll_review'),
    path('payroll/delete/<int:payroll_id>/', delete_payroll, name='delete_payroll'),
    path('view_payroll_pdf/', view_payroll_pdf, name='view_payroll_pdf'),
    path('forms/', forms, name='forms'),
    path('view_pdf2/<int:user_id>/', view_pdf2, name='view_pdf2'),
    path('view_payroll_pdf2/<int:user_id>/', view_payroll_pdf2, name='view_payroll_pdf2'),
    path('view_pdf3/<int:form_id>/', view_pdf3, name='view_pdf3'),
    path('view_payroll_pdf3/<int:form_id>/', view_payroll_pdf3, name='view_payroll_pdf3'),
    path('check_id_exists/<int:user_id>/', check_id_exists, name='check_id_exists'),
    path('api/check_email_exists/<str:email>/', check_email_exists, name='check_email_exists'),
    path('change-address/step1/', change_address_step1, name='change_address_step1'),
    path('change-address/step2/<int:form_id>/', change_address_step2, name='change_address_step2'),
    path('change-address/step3/<int:form_id>/', change_address_step3, name='change_address_step3'),
    path('change-address/step1/', change_address_step1, name='change_address_step1'),
    path('diploma/step1/', diploma_step1, name='diploma_step1'),
    path('diploma/step2/<int:diploma_id>/', diploma_step2, name='diploma_step2'),
    path('delete-address/<int:form_id>/', delete_address, name='delete_address'),
    path('delete-diploma/<int:form_id>/', delete_diploma, name='delete_diploma'),
    path('generate-change-address-pdf/<int:form_id>/', generate_change_address_pdf, name='generate_change_address_pdf'),
    path('generate-diploma-pdf/<int:diploma_id>/', generate_diploma_pdf, name='generate_diploma_pdf'),
    path('view-change-address-pdf/', view_change_address_pdf, name='view_change_address_pdf'),
    path('view-diploma-pdf/', view_diploma_pdf, name='view_diploma_pdf'),
    path('view_change_address_pdf3/<int:form_id>/', view_change_address_pdf3, name='view_change_address_pdf3'),
    path('view_diploma_pdf3/<int:form_id>/', view_diploma_pdf3, name='view_diploma_pdf3'),
    path("api/csrf/", get_csrf_token),
    path('accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

