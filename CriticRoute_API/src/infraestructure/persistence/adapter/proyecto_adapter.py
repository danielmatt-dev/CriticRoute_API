from typing import List, Optional, Dict

from django.contrib.auth.models import User
from injector import inject

from CriticRoute_API.src.core.entities.nodo_tarea import NodoTarea
from CriticRoute_API.src.core.entities.proyecto import Proyecto
from CriticRoute_API.src.core.entities.tarea import Tarea, TareaDependencia, TareaResponsable, Responsable
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

    def guardar_cpm(self, nodos: Dict[int, NodoTarea]):

        # Proyecto: Se guarda el proyecto asociado con las tareas
        proyecto_model = self._mapper.to_proyecto_model(nodos[1].tarea.proyecto)
        proyecto_model.save()

        # Tareas: Se ordenan las tareas por su número y se convierten a modelos para ser guardadas en la base de datos
        tareas_ordenadas = sorted(
            [nodo.tarea for nodo in nodos.values()],
            key=lambda tarea: tarea.numero_tarea
        )

        tareas_model = self._mapper.to_list_tarea_model(tareas_ordenadas)

        # Asocia el proyecto a cada tarea
        for tarea_model in tareas_model:
            tarea_model.proyecto = proyecto_model

        # Guarda las tareas de manera masiva
        TareaModel.objects.bulk_create(tareas_model)

        # Responsables: Se generan los responsables a partir de los nodos y se guardan en la base de datos
        responsables_model = self._mapper.to_list_responsable_model(self.__generar_responsables(nodos))

        # Guarda los responsables de manera masiva
        ResponsableModel.objects.bulk_create(responsables_model)

        dependencias_tareas = []  # Lista para almacenar las dependencias entre tareas
        relaciones_tarea_responsable = []  # Lista para almacenar las relaciones entre tareas y responsables

        # Itera sobre los nodos para establecer dependencias y relaciones
        for nodo in nodos.values():
            tarea_actual = nodo.tarea
            tarea_actual_model = self.__buscar_tarea(num_tarea=tarea_actual.numero_tarea, tareas=tareas_model)

            # Relaciona cada tarea con sus responsables
            for responsable in tarea_actual.responsables:
                responsable_model = next((responsable_model for responsable_model in responsables_model
                                          if responsable_model.nombre == responsable.nombre), None)
                if responsable_model:
                    relaciones_tarea_responsable.append(
                        TareaResponsableModel(
                            responsable=responsable_model,
                            tarea=tarea_actual_model
                        )
                    )

            # Establece las dependencias entre las tareas
            for tarea_padre in nodo.padres:
                tarea_dependencia = self.__buscar_tarea(tarea_padre.tarea.numero_tarea, tareas_model)
                if tarea_dependencia:
                    dependencias_tareas.append(
                        TareaDependenciaModel(
                            tarea_padre=tarea_dependencia,
                            tarea_hijo=tarea_actual_model
                        )
                    )

        # Guarda las dependencias entre tareas y las relaciones tarea-responsable de manera masiva
        TareaDependenciaModel.objects.bulk_create(dependencias_tareas)
        TareaResponsableModel.objects.bulk_create(relaciones_tarea_responsable)

    @staticmethod
    def __buscar_tarea(num_tarea, tareas: List[TareaModel]):
        """
        Busca una tarea en la lista de tareas por su número de tarea.

        Args:
            num_tarea (int): El número de tarea que se busca.
            tareas (List[TareaModel]): Lista de modelos de tareas en los que buscar.

        Returns:
            TareaModel: El modelo de tarea correspondiente al número de tarea, o None si no se encuentra.
        """
        return next((tarea_model for tarea_model in tareas
                    if tarea_model.numero_tarea == num_tarea), None)

    @staticmethod
    def __generar_responsables(nodos: Dict[int, NodoTarea]) -> List[Responsable]:
        """
        Genera una lista de responsables únicos a partir de los nodos del gráfico CPM.
        Se asegura de que no haya duplicados basándose en el nombre del responsable.

        Args:
            nodos (Dict[int, NodoTarea]): Diccionario de nodos del gráfico CPM
                                           y los valores son las instancias de `NodoTarea`.

        Returns:
            List[Responsable]: Lista de responsables únicos que aparecen en los nodos.
        """
        responsables_unicos = []
        nombres_responsables = []

        for nodo in nodos.values():
            for responsable in nodo.tarea.responsables:
                if responsable.nombre not in nombres_responsables:
                    responsables_unicos.append(responsable)
                    nombres_responsables.append(responsable.nombre)

        return responsables_unicos

    def guardar_proyecto(self, proyecto: Proyecto) -> Proyecto:

        proyecto_model = self._mapper.to_proyecto_model(proyecto)

        ProyectoModel.save(proyecto_model)

        return self._mapper.to_proyecto(proyecto_model)

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

    def buscar_proyectos(self, usuario: User) -> List[Proyecto]:
        models = ProyectoModel.objects.filter(usuario=usuario)
        return self._mapper.to_list_proyecto(models)

    def buscar_tareas_dependencias(self, id_proyecto: int) -> List[TareaDependencia]:
        tareas = TareaDependenciaModel.objects.filter(tarea_padre__proyecto__id_proyecto=id_proyecto)
        return self._mapper.to_list_tarea_dependencia(tareas)

    def buscar_tareas_responsables(self, id_proyecto: int) -> List[TareaResponsable]:
        responsables = TareaResponsableModel.objects.filter(tarea__proyecto__id_proyecto=id_proyecto)
        return self._mapper.to_list_tarea_responsable(responsables)

    def buscar_proyecto_por_id(self, id_proyecto: int) -> Optional[Proyecto]:
        try:

            proyecto_model = ProyectoModel.objects.get(id_proyecto=id_proyecto)

        except ProyectoModel.DoesNotExist:
            return None

        return self._mapper.to_proyecto(proyecto_model)
