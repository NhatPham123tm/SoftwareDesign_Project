from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.shortcuts import render
import msal
import requests
from django.conf import settings
from api.models import user_accs, roles
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.contrib.auth.hashers import make_password

def home(request):
    return render(request, 'home.html')

def login_page(request):
    return render(request, "login.html")

def register_page(request):
    return render(request, "register.html")

# Temporary since someone doing relate to this part
@api_view(["POST"])
@permission_classes([AllowAny])  # Allow public access to register
def user_register(request):
    """
    API-based registration for users.
    - If registering via Microsoft, password is optional.
    - If registering normally, password is required.
    """
    email = request.data.get("email")
    name = request.data.get("name")
    password = request.data.get("password", None)  # Password is optional
    role_id = request.data.get("role_id")

    if not email or not name:
        return Response({"error": "Email and name are required."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if user already exists
    if user_accs.objects.filter(email=email).exists():
        return Response({"error": "User already exists."}, status=status.HTTP_409_CONFLICT)

    # Assign default role or selected role
    if role_id:
        try:
            role = roles.objects.get(pk=role_id)
        except roles.DoesNotExist:
            return Response({"error": "Invalid role ID."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        role, _ = roles.objects.get_or_create(role_name="User")

    # Securely hash password if provided, else set a Microsoft placeholder
    password_hash = make_password(password) if password else "microsoft_auth"

    # Create the new user
    user = user_accs.objects.create(
        name=name,
        email=email,
        password_hash=password_hash,
        role=role,
    )

    return Response({
        "message": "User registered successfully!",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.role_name
        }
    }, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(user_accs, email=email)  # Get user by email
    if not check_password(password, user.password_hash):  # Verify hashed password
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    
    return Response({
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.role_name  
        }
    }, status=status.HTTP_200_OK)

    
def user_logout(request):
    logout(request)  # Clear session
    return redirect('/login')


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

# Microsoft OAuth Callback
def microsoft_callback(request):
    """Handle the OAuth callback from Microsoft."""
    if "code" not in request.GET:
        messages.error(request, "Microsoft login failed. Please try again.")
        return redirect("login")

    msal_app = get_msal_app()
    token_response = msal_app.acquire_token_by_authorization_code(
        request.GET["code"],
        scopes=["User.Read"],
        redirect_uri=settings.MICROSOFT_AUTH_REDIRECT_URI,
    )

    if "access_token" in token_response:
        # Fetch user details from Microsoft Graph API
        user_info = requests.get(
            "https://graph.microsoft.com/v1.0/me",
            headers={"Authorization": f"Bearer {token_response['access_token']}"},
        ).json()

        print("User Info:", json.dumps(user_info, indent=2))

        # Extract user details
        email = user_info.get("mail") or user_info.get("userPrincipalName")
        name = user_info.get("displayName", "Unknown User")

        if not email:
            messages.error(request, "Could not retrieve email from Microsoft. Login failed.")
            return redirect("login")

        # Check if the user exists
        user = user_accs.objects.filter(email=email).first()

        if not user:
            # Redirect new users to the registration page with prefilled email & name
            request.session["pending_email"] = email
            request.session["pending_name"] = name
            return redirect("register")  # Redirect to your registration view

        # If user exists, proceed with login
        request.session["user_id"] = user.id
        messages.success(request, f"Welcome back, {user.name}!")
        return redirect(settings.LOGIN_REDIRECT_URL)

    messages.error(request, "Microsoft login failed. Please try again.")
    return redirect("login")

# Microsoft Logout
def microsoft_logout(request):
    """Log out the user and redirect."""
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)