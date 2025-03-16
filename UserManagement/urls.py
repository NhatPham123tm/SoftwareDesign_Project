from django.contrib import admin
from django.urls import path, include
from authentication.views import home  # Import the home view
from authentication.views import microsoft_callback, dashboard, user_login, register_page ,microsoft_login,microsoft_logout, login_page, user_register, basicuser, adminpage, get_userLoad, reset_password,suspend, get_auth_data
from authentication import views
from django.contrib.auth import views as auth_views
from formProcessor.views import reimbursement_step1, reimbursement_step2, reimbursement_step3, generate_reimbursement_pdf, delete_reimbursement, view_pdf, generate_payroll_pdf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Define the root URL
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
]
