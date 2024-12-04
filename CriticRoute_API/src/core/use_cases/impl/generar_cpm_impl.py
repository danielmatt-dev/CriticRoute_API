from typing import Dict

from django.contrib.auth.models import User
from injector import inject

from CriticRoute_API.src.core.entities.enums import UnidadTiempo
from CriticRoute_API.src.core.entities.proyecto import Proyecto
from CriticRoute_API.src.core.entities.tarea import Tarea, Responsable
from CriticRoute_API.src.core.use_cases.generar_cpm import GenerarCPM
from CriticRoute_API.src.core.use_cases.grafo_cpm import GrafoCPM
from CriticRoute_API.src.core.use_cases.impl.grafo_cpm_impl import NodoTarea
from CriticRoute_API.src.core.use_cases.impl.procesador_excel_impl import ProcesadorExcelImpl


class GenerarCPMImpl(GenerarCPM):

    @inject
    def __init__(self, grafo_cpm: GrafoCPM, procesar_excel: ProcesadorExcelImpl):
        self._grafo_cpm = grafo_cpm
        self._procesar_excel = procesar_excel

    def execute(self, file_bytes: bytes, usuario: User, titulo: str, descripcion: str) -> Dict[int, NodoTarea]:

        # Establece el archivo Excel que se va a procesar
        self._procesar_excel.set_file_bytes(file_bytes)

        # Extrae los datos del proyecto desde el archivo Excel
        dic_proyecto = self._procesar_excel.extraer_datos_proyecto()

        # Crea una nueva instancia de proyecto, asociada al usuario
        proyecto = Proyecto.empty(usuario)
        proyecto.titulo = titulo
        proyecto.descripcion = descripcion
        proyecto.fecha_inicio = dic_proyecto['fecha_inicio']
        proyecto.unidad_tiempo = UnidadTiempo(dic_proyecto['unidad_tiempo'])
        proyecto.horas_trabajo_dia = dic_proyecto['horas_trabajo_dia']
        proyecto.num_decimales = dic_proyecto['numero_decimales']

        # Procesa las actividades del proyecto desde el archivo Excel
        tareas = self._procesar_excel.procesar_datos_actividades()

        # Establece el proyecto en el grafo CPM
        self._grafo_cpm.set_proyecto(proyecto)

        # Crea las tareas a partir de los datos extraídos y las agrega al grafo CPM
        for dic in tareas:
            tarea = Tarea.from_basic(
                numero_tarea=dic['ID'],
                accion=dic['Nombre'],
                descripcion=dic['Descripción'],
                tiempo_optimista=dic['Tiempos']['Optimista'],
                tiempo_probable=dic['Tiempos']['Más probable'],
                tiempo_pesimista=dic['Tiempos']['Pesimista'],
                responsables=[
                    Responsable(id_responsable=None, nombre=responsable)
                    for responsable in dic['Responsables']
                ],
                proyecto=proyecto
            )

            # Agrega la tarea al grafo CPM
            self._grafo_cpm.agregar_tarea(tarea)

        # Establece las dependencias entre tareas, basándose en las predecesoras
        for dic in tareas:
            numero_tarea_hijo: int = dic['ID']

            for padre in dic['Predecesoras']:
                numero_tarea_padre: int = padre

                # Conecta las tareas en el grafo CPM
                self._grafo_cpm.conectar_tareas(
                    numero_tarea_padre=numero_tarea_padre,
                    numero_tarea_hijo=numero_tarea_hijo)

        # Calcula el CPM (camino crítico) basado en las tareas y dependencias establecidas
        self._grafo_cpm.calcular_cpm()

        # Devuelve los nodos (tareas) del grafo CPM
        return self._grafo_cpm.get_nodos()
