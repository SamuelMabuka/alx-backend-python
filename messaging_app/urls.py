# messaging_app/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Main app (chats) API endpoints
    path('api/', include('chats.urls')),

    # Browsable API login/logout for SessionAuthentication
    path('api-auth/', include('rest_framework.urls')),

    # OAuth2 endpoints
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # JWT authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]