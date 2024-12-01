from abc import ABC, abstractmethod

from rest_framework_simplejwt.tokens import Token

from CriticRoute_API.core.entities.usuario import Usuario


# Interfaz abstracta para el caso de uso de crear un usuario.
class CrearUsuario(ABC):

    @abstractmethod
    def execute(self, usuario: Usuario) -> Token:
        """
        Método abstracto para ejecutar el proceso de creación de un usuario.

        Args:
            usuario (Usuario): El objeto que contiene la información del nuevo usuario.

        Returns:
            Token: El token generado para el nuevo usuario.
        """
        pass
