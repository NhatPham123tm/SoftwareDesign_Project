from django.utils.deprecation import MiddlewareMixin
from api.models import user_accs

class CustomAuthMiddleware(MiddlewareMixin):
    """
    Middleware to attach the user_accs instance to request.user.
    """

    def process_request(self, request):
        user_id = request.session.get("user_id")
        if user_id:
            try:
                request.user = user_accs.objects.get(id=user_id)
                request.user.is_authenticated = True  # Manually add this attribute
            except user_accs.DoesNotExist:
                request.user = None
        else:
            request.user = None
