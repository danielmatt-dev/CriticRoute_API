from abc import ABC, abstractmethod
from typing import Optional

from CriticRoute_API.src.infraestructure.delivery.dto.response.dtos import ProyectoDTO


class BuscarProyectoPorId(ABC):

    """
    Recupera las tareas, dependencias y responsables asociados a un proyecto
    y mapea la información a un DTO de Proyecto (ProyectoDTO).
    """

    @abstractmethod
    def execute(self, id_proyecto: int) -> Optional[ProyectoDTO]:
        """
        Ejecuta la lógica para buscar un proyecto por su ID y mapear los datos a un DTO.

        Args:
            id_proyecto (int): El ID del proyecto a buscar.

        Returns:
            Optional[ProyectoDTO]: El DTO que contiene la información del proyecto, tareas, dependencias y responsables.
        """
        pass
