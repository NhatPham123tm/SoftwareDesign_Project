from django.contrib import admin
from django.urls import path, include
from users.views import home  # Import the home view
from django.contrib.auth import views as auth_view
from users.views import microsoft_callback 
from users.views import dashboard, user_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Keeps user-related URLs
    path('', user_login, name='home'),  # Define the root URL
    path('auth/complete/azure/', microsoft_callback, name='microsoft-callback'),
    path('dashboard/', dashboard, name='dashboard'),
    path('api/', include('api.urls')),
]
