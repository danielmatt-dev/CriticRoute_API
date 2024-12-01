from abc import ABC, abstractmethod

from CriticRoute_API.core.entities.usuario import Usuario
from CriticRoute_API.infraestructure.delivery.dto.response.auth_token import AuthToken


class MapperDto(ABC):

    @abstractmethod
    def to_usuario(self, serializer) -> Usuario:
        pass

    @abstractmethod
    def to_auth_token(self, token) -> AuthToken:
        pass
