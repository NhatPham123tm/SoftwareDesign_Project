from django.urls import path
from . import views
from .views import microsoft_login, microsoft_callback, microsoft_logout

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    #path('logout/', views.user_logout, name='logout'),
    path('login/microsoft/', microsoft_login, name='microsoft-login'),
     path('auth/complete/azure/', microsoft_callback, name='microsoft-callback'),
    path('logout/', microsoft_logout, name='microsoft-logout'),
]
