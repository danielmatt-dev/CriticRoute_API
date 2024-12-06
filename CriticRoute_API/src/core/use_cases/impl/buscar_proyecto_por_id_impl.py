from typing import Dict, List, Tuple, Optional

from django.contrib.auth.models import User
from injector import inject

from CriticRoute_API.src.core.entities.tarea import Tarea, Responsable
from CriticRoute_API.src.core.port.proyecto_repository import ProyectoRepository
from CriticRoute_API.src.core.use_cases.buscar_proyecto_por_id import BuscarProyectoPorId
from CriticRoute_API.src.infraestructure.delivery.dto.response.dtos import ProyectoDTO, TareaDTO, ResponsableDTO


class BuscarProyectoPorIdImpl(BuscarProyectoPorId):

    @inject
    def __init__(self, repository: ProyectoRepository):
        self._repository = repository

    def execute(self, id_proyecto: int, usuario: User) -> Optional[ProyectoDTO]:

        # Recupera el proyecto desde el repositorio usando el ID
        proyecto = self._repository.buscar_proyecto_por_id(id_proyecto, usuario)

        if proyecto is None:
            return None

        # Recupera las dependencias de tareas relacionadas con el proyecto
        dependencias = self._repository.buscar_tareas_dependencias(id_proyecto)

        # Recupera los responsables de las tareas dentro del proyecto
        tareas_responsable = self._repository.buscar_tareas_responsables(id_proyecto)

        # Se inicializa el DTO del proyecto con la información básica
        dto = ProyectoDTO(
            id_proyecto=proyecto.id_proyecto,
            titulo=proyecto.titulo,
            descripcion=proyecto.descripcion,
            fecha_inicio=proyecto.fecha_inicio,
            unidad_tiempo=proyecto.unidad_tiempo.value,
            horas_trabajo_dia=proyecto.horas_trabajo_dia,
            num_decimales=proyecto.num_decimales,
            estado=proyecto.estado,
            tareas=[]
        )

        # Diccionario que almacenará las tareas agrupadas por cada tarea padre,
        # y sus respectivas tareas hijas y responsables.
        tareas_por_padre: Dict[Tarea, Tuple[List[int], List[Responsable]]] = {}

        # Agrupar las dependencias de tareas por tarea padre
        for dependencia in dependencias:

            if dependencia.tarea_padre not in tareas_por_padre:
                tareas_por_padre[dependencia.tarea_padre] = ([], [])

            tareas_por_padre[dependencia.tarea_padre][0].append(dependencia.tarea_hijo.numero_tarea)

        # Agrupar los responsables de tareas por tarea
        for tr in tareas_responsable:

            if tr.tarea not in tareas_por_padre:
                tareas_por_padre[tr.tarea] = ([], [])

            tareas_por_padre[tr.tarea][1].append(tr.responsable)

        # Se recorre el diccionario de tareas agrupadas por padre para crear el DTO de tareas
        for tarea, (hijos, responsables) in tareas_por_padre.items():
            tarea_dto = TareaDTO(
                id_tarea=tarea.id_tarea,
                numero_tarea=tarea.numero_tarea,
                accion=tarea.accion,
                notas=tarea.descripcion,
                tiempo_optimista=tarea.tiempo_optimista,
                tiempo_probable=tarea.tiempo_probable,
                tiempo_pesimista=tarea.tiempo_pesimista,
                inicio_temprano=tarea.inicio_temprano,
                duracion=tarea.duracion,
                final_temprano=tarea.final_temprano,
                inicio_tardio=tarea.inicio_tardio,
                holgura=tarea.holgura,
                final_tardio=tarea.final_tardio,
                fecha_inicio=tarea.fecha_inicio,
                fecha_final=tarea.fecha_final,
                estado=tarea.estado.value,
                responsables=[
                    ResponsableDTO(id_responsable=responsable.id_responsable, nombre=responsable.nombre)
                    for responsable in responsables
                ],
                tareas_dependencias=hijos
            )

            dto.tareas.append(tarea_dto)

        # Recupera la tarea final del proyecto
        tarea_final = self._repository.buscar_tarea_final(id_proyecto)

        # Añadir la tarea final
        dto.tareas.append(
            TareaDTO(
                id_tarea=tarea_final.id_tarea,
                numero_tarea=tarea_final.numero_tarea,
                accion=tarea_final.accion,
                notas=tarea_final.descripcion,
                tiempo_optimista=tarea_final.tiempo_optimista,
                tiempo_probable=tarea_final.tiempo_probable,
                tiempo_pesimista=tarea_final.tiempo_pesimista,
                inicio_temprano=tarea_final.inicio_temprano,
                duracion=tarea_final.duracion,
                final_temprano=tarea_final.final_temprano,
                inicio_tardio=tarea_final.inicio_tardio,
                holgura=tarea_final.holgura,
                final_tardio=tarea_final.final_tardio,
                fecha_inicio=tarea_final.fecha_inicio,
                fecha_final=tarea_final.fecha_final,
                estado=tarea_final.estado.value,
                responsables=[],
                tareas_dependencias=[]
            )
        )

        return dto
