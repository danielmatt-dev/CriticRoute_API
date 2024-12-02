from abc import ABC, abstractmethod

from CriticRoute_API.src.core.entities.usuario import Usuario
from CriticRoute_API.src.infraestructure.delivery.dto.response.auth_token import AuthToken


class MapperDto(ABC):

    """
    Interfaz para la conversión de datos entre diferentes capas del sistema.

    Esta clase define los métodos necesarios para convertir datos de un serializer
    a un objeto de entidad y viceversa.
    """

    @abstractmethod
    def to_usuario(self, serializer) -> Usuario:
        """
        Convierte un diccionario de datos en un objeto Usuario.

        Args:
            serializer (dict): Los datos del serializer recibidos.

        Returns:
            Usuario: Un objeto Usuario con los datos mapeados.
        """
        pass

    @abstractmethod
    def to_auth_token(self, token) -> AuthToken:
        """
        Convierte un token en un objeto AuthToken.

        Args:
            token (Token): El token de autenticación generado.

        Returns:
            AuthToken: Un objeto AuthToken con los valores refresh y access.
        """
        pass
