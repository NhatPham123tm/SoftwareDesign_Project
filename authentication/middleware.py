# middleware.py
##import logging
#from django.utils.deprecation import MiddlewareMixin
#from rest_framework_simplejwt.authentication import JWTAuthentication

#logger = logging.getLogger(__name__)

#class JWTAuthMiddleware(MiddlewareMixin):
#    def process_request(self, request):
#        if not request.user.is_authenticated:  # Only authenticate if user is anonymous
 #           try:
 #               auth = JWTAuthentication().authenticate(request)
 #               if auth:
  #                  request.user = auth[0]
  #          except Exception as e:
    #            logger.error(f"JWT Authentication failed: {str(e)}")##
