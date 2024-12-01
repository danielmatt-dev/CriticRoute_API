from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from CriticRoute_API.infraestructure.config.views_factory import post_crear_usuario_factory
from CriticRoute_API.infraestructure.delivery.views.views import get_csrf_token

# Definición de la ruta base para las API
api_path = 'api'

# Rutas de la aplicación, incluidas las rutas para obtener un token CSRF,
# registrar un nuevo usuario, obtener un token de acceso y refrescar el token.
urlpatterns = [
    # Ruta para el panel de administración de Django
    path('admin/', admin.site.urls),

    # Ruta para obtener el token CSRF, utilizado para proteger las solicitudes POST
    path('api/get-csrf-token/', get_csrf_token, name='get_csrf_token'),

    # Ruta para registrar un nuevo usuario mediante el endpoint /register/
    path(f'{api_path}/register/', post_crear_usuario_factory, name='crear_usuario'),

    # Ruta para obtener un par de tokens JWT (acceso y refresco) al autenticar un usuario
    path(f'{api_path}/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Ruta para refrescar el token de acceso utilizando el token de refresco
    path(f'{api_path}/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
