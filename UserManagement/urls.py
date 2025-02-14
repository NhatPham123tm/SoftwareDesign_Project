from django.contrib import admin
from django.urls import path, include
from users.views import home  # Import the home view
from django.contrib.auth import views as auth_view
from users.views import microsoft_callback 
from users.views import dashboard 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Keeps user-related URLs
    path('', home, name='home'),  # Define the root URL
    path('auth/complete/azure/', microsoft_callback, name='microsoft-callback'),
    path('dashboard/', dashboard, name='dashboard'),
]
