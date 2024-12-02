from abc import abstractmethod, ABC
from typing import List

from CriticRoute_API.core.entities.tarea import Tarea


class GrafoCPM(ABC):

    """
    Clase abstracta que define la interfaz básica para la gestión y cálculo de un grafo de tareas
    en un proyecto utilizando el método del Camino Crítico (CPM).

    Métodos abstractos:
        - agregar_tarea: Agrega una tarea al grafo.
        - conectar_tareas: Establece una relación de dependencia entre dos tareas.
        - calcular_cpm: Calcula los tiempos tempranos y tardíos de las tareas y la ruta crítica.
        - buscar_ruta_critica: Devuelve la lista de tareas que forman la ruta crítica.
    """

    @abstractmethod
    def agregar_tarea(self, tarea: Tarea):
        """
        Agrega una tarea al grafo.

        Calcula la duración de la tarea y la añade al grafo. Si la tarea ya existe, lanza un error.

        Args:
            tarea (Tarea): La tarea a agregar al grafo.

        Raises:
            ValueError: Si la tarea con el número especificado ya existe en el grafo.
        """
        pass

    @abstractmethod
    def conectar_tareas(self, numero_tarea_padre, numero_tarea_hijo):
        """
        Conecta dos tareas dentro del grafo, estableciendo una relación de dependencia.

        Args:
            numero_tarea_padre (int): El número de la tarea predecesora.
            numero_tarea_hijo (int): El número de la tarea sucesora.

        Raises:
            ValueError: Si alguno de los números de tarea no existe en el grafo.
        """
        pass

    @abstractmethod
    def calcular_cpm(self):
        """
        Calcula el Camino Crítico del proyecto.

        Este método realiza los siguientes pasos:
        - Conectar las tareas iniciales.
        - Calcular los tiempos tempranos para cada tarea.
        - Crear y conectar la tarea final.
        - Calcular los tiempos tardíos de las tareas.
        - Calcular las fechas de las tareas según la unidad de tiempo del proyecto.

        Raises:
            ValueError: Si el grafo está vacío.
        """
        pass

    @abstractmethod
    def buscar_ruta_critica(self) -> List[Tarea]:
        """
        Devuelve la lista de tareas que forman la ruta crítica del proyecto.

        La ruta crítica está compuesta por las tareas que tienen una holgura de cero.

        Returns:
            List[Tarea]: Lista de tareas que forman la ruta crítica.
        """
        pass
