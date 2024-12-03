from typing import List

from injector import inject

from CriticRoute_API.src.core.entities.proyecto import Proyecto
from CriticRoute_API.src.core.entities.tarea import Tarea, TareaDependencia, TareaResponsable, Responsable
from CriticRoute_API.src.core.entities.usuario import Usuario
from CriticRoute_API.src.core.port.proyecto_repository import ProyectoRepository
from CriticRoute_API.src.infraestructure.persistence.mapper.mapper import Mapper
from CriticRoute_API.src.infraestructure.persistence.models.models import ResponsableModel, TareaDependenciaModel, \
    TareaResponsableModel
from CriticRoute_API.src.infraestructure.persistence.models.proyecto_model import ProyectoModel
from CriticRoute_API.src.infraestructure.persistence.models.tarea_model import TareaModel


class ProyectoAdapter(ProyectoRepository):

    """
    Adaptador que implementa la interfaz de repositorio para interactuar con el modelo de datos de un proyecto.
    Proporciona operaciones para tareas, responsables, dependencias y relaciones de tareas con responsables.
    """

    @inject
    def __init__(self, mapper: Mapper):
        """
        Inicializa el adaptador de proyecto con un mapper para convertir entre las entidades y los modelos.

        Args:
            mapper (Mapper): El objeto encargado de convertir las entidades a modelos y viceversa.
        """
        self._mapper = mapper

    def guardar_tareas(self, tareas: List[Tarea]) -> List[Tarea]:

        # Convierte las tareas en modelos para persistirlas en la base de datos
        models = self._mapper.to_list_tarea_model(tareas)

        # Realiza la inserción masiva de las tareas en la base de datos
        TareaModel.objects.bulk_create(models)

        # Obtiene las tareas guardadas, filtradas por el proyecto correspondiente
        tasks = TareaModel.objects.filter(proyecto=models[0].proyecto)

        # Convierte los modelos guardados de nuevo en entidades y las retorna
        return self._mapper.to_list_tarea(tasks)

    def guardar_responsables(self, responsables: List[Responsable]) -> List[Responsable]:

        guardados = []  # Lista para almacenar los responsables que han sido guardados

        # Itera sobre los responsables, convirtiéndolos a su modelo correspondiente y guardándolos
        for responsable in responsables:
            guardado = ResponsableModel.save(self._mapper.to_responsable_model(responsable))
            guardados.append(guardado)

        # Convierte los responsables guardados en modelos de vuelta a entidades y los retorna
        return self._mapper.to_list_responsable(guardados)

    def guardar_tareas_dependencias(self, tareas: List[TareaDependencia]):
        # Convierte las dependencias en modelos y las guarda en la base de datos usando inserción masiva
        TareaDependenciaModel.objects.bulk_create(self._mapper.to_list_tarea_dependencia_model(tareas))

    def guardar_tareas_responsables(self, responsables: List[TareaResponsable]):
        # Convierte las relaciones de tareas y responsables en modelos y las guarda usando inserción masiva
        TareaResponsableModel.objects.bulk_create(self._mapper.to_list_tarea_responsable_model(responsables))

    def buscar_proyectos(self, usuario: Usuario) -> List[Proyecto]:
        models = ProyectoModel.objects.filter(usuario=self._mapper.to_usuario_model(usuario))
        return self._mapper.to_list_proyecto(models)

    def buscar_tareas_dependencias(self, id_proyecto: int) -> List[TareaDependencia]:
        tareas = TareaDependenciaModel.objects.filter(tarea_padre__proyecto__id_proyecto=id_proyecto)
        return self._mapper.to_list_tarea_dependencia(tareas)

    def buscar_tareas_responsables(self, id_proyecto: int) -> List[TareaResponsable]:
        responsables = TareaResponsableModel.objects.filter(tarea__proyecto__id_proyecto=id_proyecto)
        return self._mapper.to_list_tarea_responsable(responsables)

    def buscar_proyecto_por_id(self, id_proyecto: int) -> Proyecto:
        return self._mapper.to_proyecto(ProyectoModel.objects.filter(id_proyecto=id_proyecto))
