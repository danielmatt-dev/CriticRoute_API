from abc import ABC, abstractmethod
from typing import Dict

from CriticRoute_API.src.core.use_cases.impl.grafo_cpm_impl import NodoTarea


class GuardarGrafoCPM(ABC):

    @abstractmethod
    def execute(self, nodos: Dict[int, NodoTarea]):
        """
        Ejecuta el proceso de guardar las tareas, responsables y dependencias en la base de datos.

        Este método organiza las tareas, guarda las tareas y responsables, luego guarda las dependencias y relaciones
        entre tareas y responsables en la base de datos.

        Args:
            nodos (Dict[int, NodoTarea]): Diccionario de nodos de tarea, donde la clave es el ID de la tarea y el valor
                                          es el nodo que contiene la tarea y sus relaciones con otras tareas.
        """
        pass
