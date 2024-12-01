from abc import ABC, abstractmethod

from rest_framework_simplejwt.tokens import Token

from CriticRoute_API.core.entities.usuario import Usuario


class CrearUsuario(ABC):

    @abstractmethod
    def execute(self, usuario: Usuario) -> Token:
        pass
