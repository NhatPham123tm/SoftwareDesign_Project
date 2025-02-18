from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.shortcuts import render
import msal
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from api.models import user_accs, roles
from django.http import JsonResponse
import json
def home(request):
    return render(request, 'home.html')

# Temporary since someone doing relate to this part
def register(request):
    """Handle first-time Microsoft login users who need to complete registration."""
    email = request.session.get("pending_email", "")
    name = request.session.get("pending_name", "")

    if request.method == "POST":
        role_id = request.POST.get("role")  # Get role from form
        role = roles.objects.get(pk=role_id) if role_id else roles.objects.get_or_create(role_name="User")[0]

        # Create the new user
        user = user_accs.objects.create(
            name=name,
            email=email,
            password_hash="microsoft_auth",  # Placeholder password since authentication is via Microsoft
            role=role,
        )

        # Remove session variables
        del request.session["pending_email"]
        del request.session["pending_name"]

        # Log the user in by storing their ID in the session
        request.session["user_id"] = user.id
        messages.success(request, f"Welcome {user.name}! Your account has been registered.")
        return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, "register.html", {"email": email, "name": name})

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = user_accs.objects.get(email=email)
            if check_password(password, user.password_hash):  # Compare hashed password
                request.session["user_id"] = user.id  # Store user in session
                messages.success(request, f"Welcome {user.name}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid email or password")
        except user_accs.DoesNotExist:
            messages.error(request, "User does not exist")

    return render(request, 'login.html')

def user_logout(request):
    logout(request)  # Clear session
    return redirect('login')


def dashboard(request):
    if not getattr(request.user, 'is_authenticated', False):  # Check if user is authenticated
        return redirect('login')  # Redirect to login if not authenticated

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