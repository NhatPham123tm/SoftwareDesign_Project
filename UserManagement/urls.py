from django.contrib import admin
from django.urls import path, include
from authentication.views import home  # Import the home view
from authentication.views import microsoft_callback, dashboard, user_login, register_page ,microsoft_login,microsoft_logout, login_page, user_register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_page, name='home'),  # Define the root URL
    path('auth/complete/azure/', microsoft_callback, name='microsoft-callback'),
    path('dashboard/', dashboard, name='dashboard'),
    path('api/', include('api.urls')),
    path("register/", register_page, name="register_page"),
    path("api/user_register/", user_register, name="register"),
    path('login/microsoft/', microsoft_login, name='microsoft-login'),
    path("api/user_login/", user_login, name="api_login"),
    path('logout/', microsoft_logout, name='microsoft-logout'),
    path("login/", login_page, name="login_page"),  # Renders login.html
]
