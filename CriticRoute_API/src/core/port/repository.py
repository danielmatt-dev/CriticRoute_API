from abc import ABC, abstractmethod

from rest_framework_simplejwt.tokens import Token

from CriticRoute_API.src.core.entities.usuario import Usuario


# Interfaz abstracta para el repositorio de entre la capa de persistence y la capa de dominio.
class Repository(ABC):

    @abstractmethod
    def crear_usuario(self, usuario: Usuario) -> Token:
        """
        Método abstracto para crear un nuevo usuario en el sistema.

        Args:
            usuario (Usuario): El objeto que contiene la información del usuario.

        Returns:
            Token: El token de autenticación generado para el usuario.
        """
        pass

    @abstractmethod
    def verificar_existencia_correo(self, correo: str) -> bool:
        """
        Método abstracto para verificar si un correo electrónico ya está registrado.

        Args:
            correo (str): El correo electrónico a verificar.

        Returns:
            bool: Retorna True si el correo existe en el sistema, de lo contrario False.
        """
        pass
