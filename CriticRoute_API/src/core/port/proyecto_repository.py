from abc import ABC, abstractmethod
from typing import List, Optional, Dict

from django.contrib.auth.models import User

from CriticRoute_API.src.core.entities.nodo_tarea import NodoTarea
from CriticRoute_API.src.core.entities.proyecto import Proyecto
from CriticRoute_API.src.core.entities.tarea import Tarea, TareaDependencia, TareaResponsable, Responsable


class ProyectoRepository(ABC):

    @abstractmethod
    def guardar_proyecto(self, proyecto: Proyecto) -> Proyecto:
        """
        Guarda un proyecto en la base de datos. Si el proyecto ya existe, lo actualiza.

        Args:
            proyecto (Proyecto): El proyecto a guardar o actualizar.

        Returns:
            Proyecto: El proyecto almacenado o actualizado, con los ID generados o modificados.
        """
        pass

    @abstractmethod
    def guardar_cpm(self, nodos: Dict[int, NodoTarea]):
        """
        Guarda el grafo de tareas de un proyecto, representado por los nodos del CPM (Critical Path Method).

        Args:
            nodos (Dict[int, NodoTarea]): Diccionario que contiene los nodos de las tareas del proyecto.
        """
        pass

    @abstractmethod
    def guardar_tareas(self, tareas: List[Tarea]) -> List[Tarea]:
        """
        Guarda una lista de tareas en la base de datos. Si las tareas ya existen, se actualizan.

        Args:
            tareas (List[Tarea]): Lista de tareas a guardar.

        Returns:
            List[Tarea]: Lista de tareas almacenadas, con datos actualizados (incluyendo los ID generados).
        """
        pass

    @abstractmethod
    def guardar_responsables(self, responsables: List[Responsable]) -> List[Responsable]:
        """
        Guarda una lista de responsables en la base de datos. Si el responsable ya existe, lo omite.

        Args:
            responsables (List[Responsable]): Lista de responsables a guardar.

        Returns:
            List[Responsable]: Lista de responsables que fueron guardados.
        """
        pass

    @abstractmethod
    def guardar_tareas_dependencias(self, tareas: List[TareaDependencia]):
        """
        Guarda las dependencias entre tareas en la base de datos.

        Args:
            tareas (List[TareaDependencia]): Lista de dependencias de tareas a guardar.
        """
        pass

    @abstractmethod
    def guardar_tareas_responsables(self, responsables: List[TareaResponsable]):
        """
        Guarda la relación entre tareas y responsables en la base de datos.

        Args:
            responsables (List[TareaResponsable]): Lista de relaciones entre tareas y responsables a guardar.
        """
        pass

    @abstractmethod
    def buscar_proyectos(self, usuario: User) -> List[Proyecto]:
        """
        Busca los proyectos asociados a un usuario determinado.

        Args:
            usuario (User): El usuario cuya lista de proyectos se quiere obtener.

        Returns:
            List[Proyecto]: Una lista de entidades Proyecto asociadas al usuario.
        """
        pass

    @abstractmethod
    def buscar_tareas_dependencias(self, id_proyecto: int) -> List[TareaDependencia]:
        """
        Obtiene la lista de dependencias de tareas para un proyecto dado.

        Args:
            id_proyecto (int): El ID del proyecto para filtrar las dependencias.

        Returns:
            List[TareaDependenciaModel]: Una lista de objetos TareaDependenciaModel.
        """
        pass

    @abstractmethod
    def buscar_tareas_responsables(self, id_proyecto: int) -> List[TareaResponsable]:
        """
        Obtiene la lista de responsables de tareas para un proyecto dado.

        Args:
            id_proyecto (int): El ID del proyecto para filtrar los responsables.

        Returns:
            List[TareaResponsableModel]: Una lista de objetos TareaResponsableModel.
        """
        pass

    @abstractmethod
    def buscar_proyecto_por_id(self, id_proyecto: int, usuario: User) -> Optional[Proyecto]:
        """
        Busca un proyecto por su identificador único (id_proyecto) y lo convierte en una entidad de Proyecto.

        Args:
            id_proyecto (int): El identificador único del proyecto que se desea buscar.
            usuario (User): El usuario quien busca el proyecto

        Returns:
            Optional[Proyecto]: Una instancia de la entidad Proyecto, mapeada desde el modelo de datos.
        """
        pass

    @abstractmethod
    def buscar_tarea_final(self, id_proyecto: int) -> Optional[Tarea]:
        pass
