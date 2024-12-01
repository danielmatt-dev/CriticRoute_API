from abc import ABC, abstractmethod

from rest_framework_simplejwt.tokens import Token

from CriticRoute_API.core.entities.usuario import Usuario


class Repository(ABC):

    @abstractmethod
    def crear_usuario(self, usuario: Usuario) -> Token:
        pass

    @abstractmethod
    def verificar_existencia_correo(self, correo: str) -> bool:
        pass
