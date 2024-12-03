from abc import ABC, abstractmethod
from typing import List

from django.contrib.auth.models import User

from CriticRoute_API.src.core.entities.proyecto import Proyecto
from CriticRoute_API.src.core.entities.tarea import Tarea, TareaDependencia, TareaResponsable, Responsable
from CriticRoute_API.src.core.entities.usuario import Usuario
from CriticRoute_API.src.infraestructure.persistence.models.models import TareaDependenciaModel, ResponsableModel, \
    TareaResponsableModel
from CriticRoute_API.src.infraestructure.persistence.models.proyecto_model import ProyectoModel
from CriticRoute_API.src.infraestructure.persistence.models.tarea_model import TareaModel


class Mapper(ABC):

    @abstractmethod
    def to_usuario(self, model: User) -> Usuario:
        """
        Convierte un modelo de usuario a la entidad Usuario.

        Args:
            model (User): El modelo de usuario de la base de datos.

        Returns:
            Usuario: La entidad Usuario.
        """
        pass

    @abstractmethod
    def to_usuario_model(self, entity: Usuario) -> User:
        """
        Convierte la entidad Usuario a su modelo correspondiente para la base de datos.

        Args:
            entity (Usuario): La entidad Usuario.

        Returns:
            User: El modelo de usuario para la base de datos.
        """
        pass

    @abstractmethod
    def to_proyecto(self, model: ProyectoModel) -> Proyecto:
        """
        Convierte un modelo de proyecto a la entidad Proyecto.

        Args:
            model (ProyectoModel): El modelo de proyecto de la base de datos.

        Returns:
            Proyecto: La entidad Proyecto.
        """
        pass

    @abstractmethod
    def to_proyecto_model(self, entity: Proyecto) -> ProyectoModel:
        """
        Convierte la entidad Proyecto a su modelo correspondiente para la base de datos.

        Args:
            entity (Proyecto): La entidad Proyecto.

        Returns:
            ProyectoModel: El modelo de proyecto para la base de datos.
        """
        pass

    @abstractmethod
    def to_tarea(self, model: TareaModel) -> Tarea:
        """
        Convierte un modelo de tarea a la entidad Tarea.

        Args:
            model (TareaModel): El modelo de tarea de la base de datos.

        Returns:
            Tarea: La entidad Tarea.
        """
        pass

    @abstractmethod
    def to_tarea_model(self, entity: Tarea) -> TareaModel:
        """
        Convierte la entidad Tarea a su modelo correspondiente para la base de datos.

        Args:
            entity: (Tarea) La entidad Tarea.

        Returns:
            TareaModel: (TareaModel) El modelo de tarea para la base de datos.
        """
        pass

    @abstractmethod
    def to_list_tarea_model(self, entities: List[Tarea]) -> List[TareaModel]:
        """
        Convierte una lista de entidades Tarea a una lista de modelos TareaModel.

        Args:
            entities (List[Tarea]): Lista de entidades Tarea, que contienen los datos
            de las tareas en el dominio de la aplicación.

        Returns:
            List[TareaModel]: Lista de modelos TareaModel, que son los objetos
            que se utilizarán para interactuar con la base de datos o con la capa de almacenamiento.
        """
        pass

    @abstractmethod
    def to_list_tarea(self, models: List[TareaModel]) -> List[Tarea]:
        """
        Convierte una lista de modelos TareaModel a una lista de entidades Tarea.

        Args:
            models (List[TareaModel]): Lista de modelos TareaModel, que representan las tareas
            almacenadas en la base de datos o en otro sistema de almacenamiento.

        Returns:
            List[Tarea]: Lista de entidades Tarea, que son los objetos que contienen la lógica
            y las reglas del dominio de la aplicación.
        """
        pass

    @abstractmethod
    def to_tarea_dependencia(self, model: TareaDependenciaModel) -> TareaDependencia:
        """
        Convierte un modelo de tarea dependencia a la entidad TareaDependencia.

        Args:
            model (TareaDependenciaModel): El modelo de tarea dependencia de la base de datos.

        Returns:
            TareaDependencia: La entidad TareaDependencia.
        """
        pass

    @abstractmethod
    def to_tarea_dependencia_model(self, entity: TareaDependencia) -> TareaDependenciaModel:
        """
        Convierte la entidad TareaDependencia a su modelo correspondiente para la base de datos.

        Args:
            entity (TareaDependencia): La entidad TareaDependencia.

        Returns:
            TareaDependenciaModel: El modelo de tarea dependencia para la base de datos.
        """
        pass

    @abstractmethod
    def to_list_tarea_dependencia(self, models: List[TareaDependenciaModel]) -> List[TareaDependencia]:
        """
        Convierte una lista de modelos de tarea dependencia a una lista de entidades TareaDependencia.

        Args:
            models (List[TareaDependenciaModel]): Lista de modelos de tarea dependencia.

        Returns:
            List[TareaDependencia]: Lista de entidades TareaDependencia.
        """
        pass

    @abstractmethod
    def to_list_tarea_dependencia_model(self, entities: List[TareaDependencia]) -> List[TareaDependenciaModel]:
        """
        Convierte una lista de entidades TareaDependencia a una lista de modelos de tarea dependencia.

        Args:
            entities (List[TareaDependencia]): Lista de entidades TareaDependencia.

        Returns:
            List[TareaDependenciaModel]: Lista de modelos de tarea dependencia.
        """
        pass

    @abstractmethod
    def to_responsable(self, model: ResponsableModel) -> Responsable:
        """
        Convierte un modelo de responsable a la entidad Responsable.

        Args:
            model (ResponsableModel): El modelo de responsable de la base de datos.

        Returns:
            Responsable: La entidad Responsable.
        """
        pass

    @abstractmethod
    def to_responsable_model(self, entity: Responsable) -> ResponsableModel:
        """
        Convierte la entidad Responsable a su modelo correspondiente para la base de datos.

        Args:
            entity (Responsable): La entidad Responsable.

        Returns:
            ResponsableModel: El modelo de responsable para la base de datos.
        """
        pass

    @abstractmethod
    def to_list_responsable(self, models: List[ResponsableModel]) -> List[Responsable]:
        """
        Convierte una lista de modelos de responsables a una lista de entidades Responsable.

        Args:
            models (List[ResponsableModel]): Lista de modelos de responsables.

        Returns:
            List[Responsable]: Lista de entidades Responsable.
        """
        pass

    @abstractmethod
    def to_list_responsable_model(self, entities: List[Responsable]) -> List[ResponsableModel]:
        """
        Convierte una lista de entidades Responsable a una lista de modelos de responsables.

        Args:
            entities (List[Responsable]): Lista de entidades Responsable.

        Returns:
            List[ResponsableModel]: Lista de modelos de responsables.
        """
        pass

    @abstractmethod
    def to_tarea_responsable(self, model: TareaResponsableModel) -> TareaResponsable:
        """
        Convierte un modelo de tarea responsable a la entidad TareaResponsable.

        Args:
            model (TareaResponsableModel): El modelo de tarea responsable de la base de datos.

        Returns:
            TareaResponsable: La entidad TareaResponsable.
        """
        pass

    @abstractmethod
    def to_tarea_responsable_model(self, entity: TareaResponsable) -> TareaResponsableModel:
        """
        Convierte la entidad TareaResponsable a su modelo correspondiente para la base de datos.

        Args:
            entity (TareaResponsable): La entidad TareaResponsable.

        Returns:
            TareaResponsableModel: El modelo de tarea responsable para la base de datos.
        """
        pass

    @abstractmethod
    def to_list_tarea_responsable(self, models: List[TareaResponsableModel]) -> List[TareaResponsable]:
        """
        Convierte una lista de modelos de tarea responsable a una lista de entidades TareaResponsable.

        Args:
            models (List[TareaResponsableModel]): Lista de modelos de tarea responsable.

        Returns:
            List[TareaResponsable]: Lista de entidades TareaResponsable.
        """
        pass

    @abstractmethod
    def to_list_tarea_responsable_model(self, entities: List[TareaResponsable]) -> List[TareaResponsableModel]:
        """
        Convierte una lista de entidades TareaResponsable a una lista de modelos de tarea responsable.

        Args:
            entities (List[TareaResponsable]): Lista de entidades TareaResponsable.

        Returns:
            List[TareaResponsableModel]: Lista de modelos de tarea responsable.
        """
        pass

    @abstractmethod
    def to_list_proyecto(self, models: List[ProyectoModel]) -> List[Proyecto]:
        """
        Convierte una lista de modelos ProyectoModel a una lista de entidades Proyecto.

        Args:
            models (List[ProyectoModel]): Lista de modelos ProyectoModel.

        Returns:
            List[Proyecto]: Lista de entidades Proyecto.
        """
        pass

    @abstractmethod
    def to_list_proyecto_model(self, entities: List[Proyecto]) -> List[ProyectoModel]:
        """
        Convierte una lista de entidades Proyecto a una lista de modelos ProyectoModel.

        Args:
            entities (List[Proyecto]): Lista de entidades Proyecto.

        Returns:
            List[ProyectoModel]: Lista de modelos ProyectoModel.
        """
        pass
