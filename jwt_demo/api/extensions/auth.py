from rest_framework.authentication import BaseAuthentication

class JwtQueryParamsAuthentication(BaseAuthentication):
    def authenticate(self, request):
        pass
