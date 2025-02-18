from django.contrib import admin
from django.urls import path, include
from authentication.views import home  # Import the home view
from authentication.views import microsoft_callback, dashboard, user_login, register,microsoft_login,microsoft_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_login, name='home'),  # Define the root URL
    path('auth/complete/azure/', microsoft_callback, name='microsoft-callback'),
    path('dashboard/', dashboard, name='dashboard'),
    path('api/', include('api.urls')),
    path("register/", register, name="register"),
    path('login/microsoft/', microsoft_login, name='microsoft-login'),
    path('login/', user_login, name='login'),
    path('logout/', microsoft_logout, name='microsoft-logout'),
]
