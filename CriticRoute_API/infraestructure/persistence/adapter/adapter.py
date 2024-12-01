from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import Token, RefreshToken

from CriticRoute_API.core.entities.usuario import Usuario
from CriticRoute_API.core.port.repository import Repository


# Implementación del repositorio de autenticación usando Django ORM.
class Adapter(Repository):

    def crear_usuario(self, usuario: Usuario) -> Token:

        # Crea un nuevo usuario y lo guarda en la base de datos
        user = User.objects.create_user(
            username=usuario.username,
            email=usuario.email,
            password=usuario.password
        )

        # Generación del token de acceso para el usuario creado.
        return RefreshToken.for_user(user)

    def verificar_existencia_correo(self, correo: str) -> bool:
        return User.objects.filter(email=correo).exists()