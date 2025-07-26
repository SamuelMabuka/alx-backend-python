from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # App-specific API endpoints
    path('api/', include('chats.urls')),

    # Browsable API login/logout (SessionAuth)
    path('api-auth/', include('rest_framework.urls')),

    # OAuth2 endpoints
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # JWT token authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
