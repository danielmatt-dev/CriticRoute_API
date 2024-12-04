from typing import Dict

from injector import inject

from CriticRoute_API.src.core.port.proyecto_repository import ProyectoRepository
from CriticRoute_API.src.core.use_cases.guardar_grafo_cpm import GuardarGrafoCPM
from CriticRoute_API.src.core.use_cases.impl.grafo_cpm_impl import NodoTarea


class GuardarGrafoCPMImpl(GuardarGrafoCPM):

    """
    Implementación del servicio para guardar un grafo de tareas dentro de un proyecto.

    Este servicio se encarga de almacenar las tareas, los responsables de las tareas, las dependencias entre las tareas
    y las relaciones de tareas-responsables en la base de datos.

    Asegura que las tareas y sus responsables sean persistidos antes de guardar las dependencias.
    """

    @inject
    def __init__(self, repository: ProyectoRepository):
        """
        Inicializa el servicio con un repositorio de proyecto para interactuar con la base de datos.

        Args:
            repository (ProyectoRepository): Repositorio que maneja la persistencia de proyectos, tareas y responsables.
        """
        self._repository = repository

    def execute(self, nodos: Dict[int, NodoTarea]):
        self._repository.guardar_cpm(nodos)
