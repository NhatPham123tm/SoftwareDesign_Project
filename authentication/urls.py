from django.urls import path
from .views import microsoft_login, microsoft_callback, microsoft_logout, user_login, login_page, register_page, user_register, dashboard, home, admin, basicuser, adminpage, get_userLoad, get_auth_data, forms
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", register_page, name="register_page"),
    path("api/user_register/", user_register, name="register"),
    #path('logout/', views.user_logout, name='logout'),
    path('login/microsoft/', microsoft_login, name='microsoft-login'),
    path('auth/complete/azure/', microsoft_callback, name='microsoft-callback'),
    path('logout/', microsoft_logout, name='microsoft-logout'),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # Refresh JWT Token
    path("login/", login_page, name="login_page"),  # Renders login.html
    path("api/user_login/", user_login, name="api_login"),
    path('dashboard/', dashboard, name='dashboard'),
    path('basicuser/', basicuser, name='basicuser'),
    path('home/', home, name='home'),
    path('adminpage/', adminpage, name='adminpage'),
    path('api/get_userLoad/', get_userLoad, name='get_userLoad'),
    path("api/microsoft-login/", get_auth_data, name="microsoft-login-json"),
    path('forms/', forms, name='forms'),
]
