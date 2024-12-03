from typing import Dict

from injector import inject

from CriticRoute_API.src.core.entities.tarea import TareaDependencia, TareaResponsable
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

        # Ordena las tareas por su número de tarea para asegurarse de que se guardan en el orden correcto
        tareas_ordenadas = sorted(
            [nodo.tarea for nodo in nodos.values()],
            key=lambda tarea: tarea.numero_tarea)

        # Extrae los responsables únicos de todas las tareas del grafo (sin duplicados)
        responsables_unicos = set(responsable for nodo in nodos.values() for responsable in nodo.tarea.responsables)

        # Guarda las tareas y los responsables en la base de datos
        tareas_guardadas = self._repository.guardar_tareas(tareas_ordenadas)
        responsables_guardados = self._repository.guardar_responsables(list(responsables_unicos))

        # Inicializa las listas para almacenar las dependencias y las relaciones tarea-responsable
        dependencias_tareas = []
        relaciones_tarea_responsable = []

        # Recorre los nodos y procesa cada tarea
        for nodo in nodos.values():
            tarea_actual = nodo.tarea

            # Guarda las relaciones entre tareas y responsables
            for responsable in tarea_actual.responsables:
                responsable_guardado = next(
                    (responsable_guardado for responsable_guardado in responsables_guardados if
                     responsable_guardado.nombre == responsable.nombre), None)
                if responsable_guardado:
                    relaciones_tarea_responsable.append(
                        TareaResponsable(
                            id_tarea_responsable=None,
                            tarea=tarea_actual,
                            responsable=responsable_guardado))

            # Guarda las dependencias entre tareas
            for tarea_padre in nodo.padres:
                tarea_dependencia = next(
                    (tarea_guardada for tarea_guardada in tareas_guardadas if
                     tarea_guardada.numero_tarea == tarea_padre.tarea.numero_tarea), None)
                if tarea_dependencia:
                    dependencias_tareas.append(
                        TareaDependencia(
                            id_tarea_dependencia=None,
                            tarea_padre=tarea_dependencia,
                            tarea_hijo=tarea_actual))

        # Guarda las dependencias y las relaciones tarea-responsable en la base de datos
        self._repository.guardar_tareas_dependencias(dependencias_tareas)
        self._repository.guardar_tareas_responsables(relaciones_tarea_responsable)
