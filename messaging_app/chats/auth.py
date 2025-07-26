# expose token endpoints using DRF SimpleJWT views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)