from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Example of a custom JWT authentication class.
    Extend this if you want to log, restrict, or debug token behavior.
    """
    pass
