from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.shortcuts import render
import msal
import requests
from django.conf import settings
from api.models import user_accs, ReimbursementRequest, PayrollAssignment
from django.contrib.auth.decorators import user_passes_test
import json
from django.contrib.auth.decorators import user_passes_test
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .serializers import UserRegisterSerializer, UserLoginSerializer
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from api.serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'home.html')

def login_page(request):
    return render(request, "login.html")

def register_page(request):
    return render(request, "register.html")

def basicuser(request):
    return render(request, 'basicuser.html')

def forms(request):
    reimbursement = ReimbursementRequest.objects.filter(user=request.user).order_by('-created_at')[:5]
    payroll = PayrollAssignment.objects.filter(user=request.user).order_by('-created_at')[:5]
    past_payrolls = payroll[1:] if payroll.count() > 1 else []
    past_reimbursements = reimbursement[1:] if reimbursement.count() > 1 else []
    return render(request, "forms.html", {'reimbursement': reimbursement,'payroll': payroll, 'past_payroll': past_payrolls, 'past_reimbursement': past_reimbursements})

def is_admin(user):
    print(user)
    if not user.is_authenticated:
        return False
    return getattr(user, 'role_id', None) == 1


@login_required
@user_passes_test(is_admin)
def adminpage(request):
    print(f"Session Key: {request.session.session_key}")
    print(f"User: {request.user}")
    print(f"Is Authenticated: {request.user.is_authenticated}")
    return render(request, 'admin.html')

def get_userLoad(request):
    users = user_accs.objects.select_related('role').all()
    serializer = UserSerializer(users, many=True)
    return JsonResponse({'users': serializer.data})

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
                "role": user.role_id
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        "message": "Registration failed.",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]
        login(request, user)
        request.session.save()  # Explicitly save the session
        #print(f"User {user.email} logged in. Session: {request.session.session_key}")
        #print(f"Session exists: {request.session.exists(request.session.session_key)}")
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "message": "Logged in successfully",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role_id,
                "status": user.status,
            }
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


def user_logout(request):
    storage = messages.get_messages(request)
    storage.used = True 
    logout(request)
    return redirect('/login')

@login_required
def dashboard(request):
    reimbursement = ReimbursementRequest.objects.filter(user=request.user).exclude(status="Approved").first()
    payroll = PayrollAssignment.objects.filter(user=request.user).exclude(status="Approved").first()
    return render(request, 'dashboard.html', {'reimbursement': reimbursement,'payroll': payroll},)

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

# Hnadle after microsoft login
def microsoft_callback(request):
    """Handle Microsoft OAuth callback and issue JWT tokens."""
    if "code" not in request.GET:
        messages.error(request, "Microsoft login failed. Please try again.")
        return redirect("/login")

    msal_app = get_msal_app()
    token_response = msal_app.acquire_token_by_authorization_code(
        request.GET["code"],
        scopes=["User.Read"],
        redirect_uri=settings.MICROSOFT_AUTH_REDIRECT_URI,
    )

    if "access_token" not in token_response:
        error_msg = token_response.get("error_description", "Unknown error")
        messages.error(request, f"Microsoft login failed: {error_msg}")
        return redirect("/login")

    # Fetch user details from Microsoft Graph API
    user_info = requests.get(
        "https://graph.microsoft.com/v1.0/me",
        headers={"Authorization": f"Bearer {token_response['access_token']}"},
    ).json()

    email = (user_info.get("mail") or user_info.get("userPrincipalName")).lower()
    name = user_info.get("displayName", "Unknown User")

    if not email:
        messages.error(request, "Could not retrieve email from Microsoft. Login failed.")
        return redirect("/login")

    # Retrieve 'id' and 'password' from cookies
    id = request.COOKIES.get("sessionId")
    password = request.COOKIES.get("password")
    # Check if user exists, otherwise create one
    try:
        user = user_accs.objects.get(email=email)
    except user_accs.DoesNotExist:
        # Create new user if doesn't exist
        if user_accs.DoesNotExist:
            if not id or not password:
                messages.error(request, "No account registered with this Microsoft email")
                return redirect('register_page')
        
        user = user_accs.objects.create(
            id=id,
            email=email,
            name=name
        )
        user.set_password(password)  # Hash and store password
        user.save()

    # Authenticate & log in user
    user.backend = "django.contrib.auth.backends.ModelBackend"
    login(request, user)
    request.session.save()
    # Generate JWT Tokens
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # Check if request expects JSON response
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
                "status": user.status
            }
        }, status=200)
    #save json response
    request.session["auth_data"] = {
        "access_token": access_token,
        "refresh_token": str(refresh),
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role_id if user.role_id else "2",
            "status": user.status
        }
    }
    
    # Clear cookies after user creation and login
    if user.status == "active":
        response = redirect(f"/dashboard/")
    else:
        response = redirect("/suspend")
    
    response.delete_cookie('sessionId')
    response.delete_cookie('password')

    # Store JWT tokens in session for frontend redirection (if necessary)
    request.session["access_token"] = access_token
    request.session["refresh_token"] = str(refresh)
    #print(f"User {user.email} logged in. Session: {request.session.session_key}")
    #print(f"Session exists: {request.session.exists(request.session.session_key)}")
    messages.success(request, f"Welcome back, {user.name}!")
    return response

def get_auth_data(request):
    """Retrieve stored authentication data from session."""
    auth_data = request.session.get("auth_data", None)
    
    if not auth_data:
        return JsonResponse({"error": "No authentication data found"}, status=401)
    
    return JsonResponse(auth_data, status=200)

# Microsoft Logout
def microsoft_logout(request):
    """Log out the user and redirect."""
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)

def suspend(request):
    return render(request, 'suspend.html')


# Simplified process without checking through user email
def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check that passwords match
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'reset_password.html')

        try:
            # Look up the user by email
            user = user_accs.objects.get(email=email)
        except user_accs.DoesNotExist:
            messages.error(request, "No account found with that email address.")
            return render(request, 'reset_password.html')

        # Update the password (make sure you hash it)
        user.password_hash = make_password(new_password)
        user.save()

        messages.success(request, "Password reset successfully. Please log in with your new password.")
        return redirect('/login') 

    # For GET requests, just display the form
    return render(request, 'reset_password.html')

@api_view(["GET"])
def check_id_exists(request, user_id):
    # Check if the user ID exists in the database
    id_exists = user_accs.objects.filter(id=user_id).exists()

    # Return response based on whether the ID is unique or already taken
    return JsonResponse({'isUnique': not id_exists})

@api_view(["GET"])
def check_email_exists(request, email):
    email_exists = user_accs.objects.filter(email=email).exists()
    return JsonResponse({'isUnique': not email_exists})