from abc import ABC, abstractmethod
from typing import List

from CriticRoute_API.src.core.entities.proyecto import Proyecto
from CriticRoute_API.src.core.entities.usuario import Usuario
from CriticRoute_API.src.infraestructure.delivery.dto.response.auth_token import AuthToken
from CriticRoute_API.src.infraestructure.delivery.dto.response.dtos import ProyectoDTO


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

    @abstractmethod
    def to_proyecto_dto(self, proyecto: Proyecto) -> ProyectoDTO:
        """
        Método abstracto que debe ser implementado para convertir un objeto `Proyecto` a un DTO `ProyectoDTO`.

        Args:
            proyecto (Proyecto): El objeto `Proyecto` a transformar.

        Returns:
            ProyectoDTO: El objeto DTO que representa el `Proyecto`.
        """
        pass

    @abstractmethod
    def to_list_proyecto_dto(self, proyectos: List[Proyecto]) -> List[ProyectoDTO]:
        """
        Método abstracto que debe ser implementado para convertir una lista de objetos `Proyecto`
        a una lista de DTOs `ProyectoDTO`.

        Args:
            proyectos (List[Proyecto]): Lista de objetos `Proyecto` a transformar.

        Returns:
            List[ProyectoDTO]: Lista de objetos `ProyectoDTO` que representan los `Proyecto` de entrada.
        """
        pass
