from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegisterForm
from django.shortcuts import render
import msal
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, "dashboard.html")

@login_required
def login_success(request):
    return redirect('/dashboard/')

@login_required
def check_session(request):
    return JsonResponse({"user": request.user.username, "authenticated": request.user.is_authenticated})

# Initialize MSAL
def get_msal_app():
    return msal.ConfidentialClientApplication(
        settings.MICROSOFT_AUTH_CLIENT_ID,
        authority=settings.MICROSOFT_AUTHORITY,
        client_credential=settings.MICROSOFT_AUTH_CLIENT_SECRET,
    )

# Microsoft Login
def microsoft_login(request):
    msal_app = get_msal_app()
    auth_url = msal_app.get_authorization_request_url(
        ["User.Read"],
        redirect_uri=settings.MICROSOFT_AUTH_REDIRECT_URI,
    )
    return redirect(auth_url)

# Microsoft OAuth Callback
def microsoft_callback(request):
    if "code" not in request.GET:
        return redirect("login")

    msal_app = get_msal_app()
    token_response = msal_app.acquire_token_by_authorization_code(
        request.GET["code"],
        scopes=["User.Read"],
        redirect_uri=settings.MICROSOFT_AUTH_REDIRECT_URI,
    )
    #print("Token Response:", json.dumps(token_response, indent=2))
    if "access_token" in token_response:
        user_info = requests.get(
            "https://graph.microsoft.com/v1.0/me",
            headers={"Authorization": f"Bearer {token_response['access_token']}"},
        ).json()

        # Get or create the user
        user, _ = User.objects.get_or_create(
            username=user_info["userPrincipalName"],
            defaults={"first_name": user_info.get("givenName", ""), "last_name": user_info.get("surname", "")},
        )
        login(request, user)
        print("User authenticated:", request.user.is_authenticated)
        messages.success(request, f"Welcome {user.first_name}! You have logged in successfully.")
        print("Redirecting to:", settings.LOGIN_REDIRECT_URL)
        return redirect(settings.LOGIN_REDIRECT_URL)
    messages.error(request, "Microsoft login failed. Please try again.")
    return redirect("login")

# Microsoft Logout
def microsoft_logout(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


def basicuser(request):
    return render(request, 'basicuser.html')

def admin(request):
    return render(request, 'admin.html')

def suspend(request):
    return render(request, 'suspend.html')
