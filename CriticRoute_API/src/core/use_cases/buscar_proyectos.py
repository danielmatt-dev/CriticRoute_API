from abc import ABC, abstractmethod
from typing import List

from django.contrib.auth.models import User

from CriticRoute_API.src.core.entities.proyecto import Proyecto


class BuscarProyectos(ABC):

    """
    Se encarga de la lógica de negocio para buscar proyectos de un usuario específico.
    """

    @abstractmethod
    def execute(self, usuario: User) -> List[Proyecto]:
        """
        Ejecuta la lógica de negocio para obtener todos los proyectos asociados a un usuario específico.

        Este método se encarga de delegar la tarea de buscar los proyectos al repositorio,
        que consultará la base de datos y devolverá una lista de proyectos.

        Args:
            usuario (User): El usuario cuyo proyectos deben ser obtenidos.

        Returns:
            List[Proyecto]: Una lista de proyectos asociados al usuario.
        """
        pass
