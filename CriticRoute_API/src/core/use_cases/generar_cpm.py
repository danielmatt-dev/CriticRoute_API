from abc import ABC, abstractmethod
from typing import Dict

from django.contrib.auth.models import User

from CriticRoute_API.src.core.entities.nodo_tarea import NodoTarea


class GenerarCPM(ABC):

    """
    Lógica para generar el gráfico de ruta crítica (CPM) a partir de un archivo Excel.
    Extrae los datos del proyecto y las actividades, construye las tareas, y calcula la ruta crítica.
    """
    @abstractmethod
    def execute(self, file_bytes: bytes, usuario: User, titulo: str, descripcion: str) -> Dict[int, NodoTarea]:
        """
        Ejecuta el proceso de generación del CPM a partir de los bytes del archivo Excel. Extrae los datos del proyecto
        y las actividades, y luego construye las tareas y las relaciones entre ellas. Finalmente, calcula la ruta
        crítica del proyecto.

        Args:
            file_bytes (bytes): Los bytes del archivo Excel que contiene los datos del proyecto y las actividades.
            usuario (User): El usuario que solicita la creación del CPM. Utilizado para asociar el proyecto al usuario.
            titulo (str): El título del proyecto a crear.
            descripcion (str): La descripción del proyecto a crear.

        Returns:
            Dict[int, NodoTarea]: Diccionario de nodos que representa el grafo de tareas
                                   y el valor es la instancia de `NodoTarea` correspondiente.
        """
        pass
