from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from CriticRoute_API.infraestructure.config.views_factory import post_crear_usuario_factory
from CriticRoute_API.infraestructure.delivery.views.views import get_csrf_token

api_path = 'api'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/get-csrf-token/', get_csrf_token, name='get_csrf_token'),
    path(f'{api_path}/register/', post_crear_usuario_factory, name='crear_usuario'),
    path(f'{api_path}/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f'{api_path}/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
