from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.shortcuts import render
import msal
import requests
from django.conf import settings
from api.models import user_accs, roles
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.decorators import user_passes_test
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .serializers import UserRegisterSerializer, UserLoginSerializer
from django.http import JsonResponse

def home(request):
    return render(request, 'home.html')

def login_page(request):
    return render(request, "login.html")

def register_page(request):
    return render(request, "register.html")

def basicuser(request):
    return render(request, 'basicuser.html')

def is_admin(user):
    # Ensure the user is authenticated and has role id 1
    return getattr(user, 'role', None) and user.role_id == 1

@authentication_classes([JWTAuthentication])  # Use JWT authentication
@permission_classes([IsAuthenticated])  # Allow only authenticated users
@user_passes_test(is_admin)
def admin(request):
    return render(request, 'admin.html')

# Temporary since someone doing relate to this part
@api_view(["POST"])
@permission_classes([AllowAny])  # Allow public access to register
def user_register(request):
    """
    API-based registration using serializers.
    """
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            "message": "User registered successfully!",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role_id # returns the role ID
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    """
    API-based login using serializers.
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role_id
            }
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)



def user_logout(request):
    logout(request)  # Clear session
    return redirect('/login')


@authentication_classes([JWTAuthentication])  # Use JWT authentication
@permission_classes([IsAuthenticated])  # Allow only authenticated users
def dashboard(request):
    return render(request, "dashboard.html", {"user": request.user})


def login_success(request):
    redirect(settings.LOGIN_REDIRECT_URL)



# Initialize MSAL
def get_msal_app():
    return msal.ConfidentialClientApplication(
        settings.MICROSOFT_AUTH_CLIENT_ID,
        authority=settings.MICROSOFT_AUTHORITY,
        client_credential=settings.MICROSOFT_AUTH_CLIENT_SECRET,
    )

def get_msal_app():
    """Returns a configured MSAL ConfidentialClientApplication instance."""
    return msal.ConfidentialClientApplication(
        settings.MICROSOFT_AUTH_CLIENT_ID,
        authority=settings.MICROSOFT_AUTHORITY,
        client_credential=settings.MICROSOFT_AUTH_CLIENT_SECRET,
    )

# Microsoft Login
def microsoft_login(request):
    """Redirect the user to Microsoft's login page."""
    msal_app = get_msal_app()
    auth_url = msal_app.get_authorization_request_url(
        scopes=["User.Read"],
        redirect_uri=settings.MICROSOFT_AUTH_REDIRECT_URI,
    )
    return redirect(auth_url)

def microsoft_callback(request):
    """Handle Microsoft OAuth callback and issue JWT tokens."""
    if "code" not in request.GET:
        messages.error(request, "Microsoft login failed. Please try again.")
        return redirect("login")

    msal_app = get_msal_app()
    token_response = msal_app.acquire_token_by_authorization_code(
        request.GET["code"],
        scopes=["User.Read"],
        redirect_uri=settings.MICROSOFT_AUTH_REDIRECT_URI,
    )

    if "access_token" not in token_response:
        error_msg = token_response.get("error_description", "Unknown error")
        messages.error(request, f"Microsoft login failed: {error_msg}")
        return redirect("login")

    # Fetch user details from Microsoft Graph API
    user_info = requests.get(
        "https://graph.microsoft.com/v1.0/me",
        headers={"Authorization": f"Bearer {token_response['access_token']}"},
    ).json()

    email = user_info.get("mail") or user_info.get("userPrincipalName")
    name = user_info.get("displayName", "Unknown User")

    if not email:
        messages.error(request, "Could not retrieve email from Microsoft. Login failed.")
        return redirect("login")

    # Check if user exists, otherwise create one
    user, created = user_accs.objects.get_or_create(email=email, defaults={"name": name})

    if created:
        user.set_password(None)  # External account (no password needed)
        user.save()

    # Authenticate & log in user
    user.backend = "django.contrib.auth.backends.ModelBackend"
    login(request, user)

    # Generate JWT Tokens
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # Check if request expects JSON response
    if request.headers.get("Accept") == "application/json":
        return JsonResponse({
            "access_token": access_token,
            "refresh_token": str(refresh),
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role_id if user.role_id else "2",
            }
        }, status=200)

    # Store JWT tokens in session for frontend redirection (if necessary)
    request.session["access_token"] = access_token
    request.session["refresh_token"] = str(refresh)

    messages.success(request, f"Welcome back, {user.name}!")
    if user.role_id == 2:
        return redirect(f"/dashboard/?token={access_token}")
    else:
        return redirect(f"/admin/?token={access_token}")

# Microsoft Logout
def microsoft_logout(request):
    """Log out the user and redirect."""
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)

def suspend(request):
    return render(request, 'suspend.html')