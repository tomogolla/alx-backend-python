from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions, authentication
# from django.contrib.auth import views as auth_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
   openapi.Info(
      title="ALX Travel App API",
      default_version='v1',
      description="API documentation for the ALX Travel Application",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@alxtravelapp.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=False,
   permission_classes=[permissions.IsAuthenticated],
    authentication_classes=[authentication.BasicAuthentication],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),
    # path('api-auth/', include('rest_framework.urls')), # For browsable API login/logout
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
