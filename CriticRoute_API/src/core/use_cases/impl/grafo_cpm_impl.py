from datetime import timedelta
from typing import List, Dict, Optional

from CriticRoute_API.src.core.entities.nodo_tarea import NodoTarea
from CriticRoute_API.src.core.entities.proyecto import Proyecto
from CriticRoute_API.src.core.entities.enums import UnidadTiempo
from CriticRoute_API.src.core.entities.tarea import Tarea
from CriticRoute_API.src.core.use_cases.grafo_cpm import GrafoCPM


class GrafoCPMImpl(GrafoCPM):

    def __init__(self):
        super().__init__()
        self.__nodos: Dict[int, NodoTarea] = {}
        self.__tarea_inicial = NodoTarea(Tarea.empty())
        self.__tarea_final = NodoTarea(Tarea.empty())
        self.__proyecto = None

        # Configurar tarea inicial
        self.__tarea_inicial.tarea.numero_tarea = 0
        self.__tarea_inicial.tarea.accion = "Inicio"
        self.__tarea_inicial.tarea.inicio_temprano = 0
        self.__tarea_inicial.tarea.final_temprano = 0
        self.__tarea_inicial.tarea.duracion = 0

    def get_proyecto(self) -> Optional[Proyecto]:
        return self.__proyecto

    def set_proyecto(self, proyecto: Proyecto):
        self.__proyecto = proyecto

    def agregar_tarea(self, tarea: Tarea):

        tarea.calcular_duracion()

        # Verifica si la tarea ya está en el grafo
        if tarea.numero_tarea in self.__nodos:
            raise ValueError(f"Tarea con número {tarea.numero_tarea} ya existe.")

        # Agrega el nodo de la tarea al grafo
        self.__nodos[tarea.numero_tarea] = NodoTarea(tarea)

    def conectar_tareas(self, numero_tarea_padre, numero_tarea_hijo):
        if numero_tarea_padre not in self.__nodos or numero_tarea_hijo not in self.__nodos:
            raise ValueError("Uno de los nodos no existe en el grafo.")

        # Obtiene los nodos correspondientes
        padre = self.__nodos[numero_tarea_padre]
        hijo = self.__nodos[numero_tarea_hijo]

        # Establece la relación de dependencia
        padre.hijos.append(hijo)
        hijo.padres.append(padre)

    def calcular_cpm(self):
        if not self.__nodos:
            raise ValueError("El grafo está vacío. No hay tareas para calcular.")

        # Conectar tareas iniciales
        self.__conectar_tarea_iniciales()

        # Calcular tiempos tempranos
        self.__calcular_tiempos_tempranos()

        # Crear y conectar la tarea final
        self.__crear_tarea_final()

        # Calcular tiempos tardíos
        self.__calcular_tiempos_tardios()

        # Calcular fechas tardías
        self.__calcular_fecha_tareas()

    def __conectar_tarea_iniciales(self):

        """
        Conecta la tarea inicial con todas las tareas que no tienen tareas predecesoras.

        Esta operación es necesaria para asegurar que el grafo tenga un punto de inicio válido.
        """

        for nodo in self.__nodos.values():
            if not nodo.padres:
                nodo.padres.append(self.__tarea_inicial)
                self.__tarea_inicial.hijos.append(nodo)

    def __calcular_tiempos_tempranos(self):

        """
        Calcula los tiempos tempranos de inicio y finalización de todas las tareas.

        Si una tarea no tiene tareas predecesoras, su inicio temprano es cero. Para otras tareas,
        su inicio temprano es el máximo de los tiempos de finalización tempranos de sus predecesoras.
        """

        for nodo in self.__nodos.values():

            if not nodo.padres:
                nodo.tarea.inicio_temprano = 0
            else:
                nodo.tarea.inicio_temprano = round(
                    max(padre.tarea.final_temprano for padre in nodo.padres),
                    self.__proyecto.num_decimales)

            nodo.tarea.final_temprano = round(
                nodo.tarea.inicio_temprano + nodo.tarea.duracion,
                self.__proyecto.num_decimales)

    def __crear_tarea_final(self):

        """
        Crea la tarea final y la conecta a todas las tareas que no tienen tareas sucesoras.

        La tarea final es la última tarea en el grafo, y su tiempo de inicio y finalización es
        calculado a partir de las tareas predecesoras.
        """

        # Asigna número de tarea y acción a la tarea final
        self.__tarea_final.tarea.numero_tarea = max(self.__nodos.keys()) + 1
        self.__tarea_final.tarea.accion = 'Final'

        # Conecta la tarea final con las tareas que no tienen sucesores
        for nodo in self.__nodos.values():
            if not nodo.hijos:
                nodo.hijos.append(self.__tarea_final)
                self.__tarea_final.padres.append(nodo)

        # Calcula los tiempos de inicio y finalización tempranos de la tarea final
        self.__tarea_final.tarea.inicio_temprano = round(max(
            nodo.tarea.final_temprano for nodo in self.__tarea_final.padres),
            self.__proyecto.num_decimales)
        self.__tarea_final.tarea.final_temprano = round(
            self.__tarea_final.tarea.inicio_temprano,
            self.__proyecto.num_decimales)

    def __calcular_tiempos_tardios(self):

        """
        Calcula los tiempos tardíos de inicio y finalización de las tareas.

        Los tiempos tardíos se calculan comenzando desde la tarea final y trabajando hacia atrás.
        Si una tarea tiene sucesores, su tiempo tardío es el mínimo de los tiempos de inicio tardíos
        de sus sucesores.
        """

        if not self.__tarea_final:
            raise ValueError("No se ha definido la tarea final.")

        # Establece los tiempos tardíos de la tarea final
        self.__tarea_final.tarea.final_tardio = round(
            self.__tarea_final.tarea.final_temprano,
            self.__proyecto.num_decimales)
        self.__tarea_final.tarea.inicio_tardio = round(
            self.__tarea_final.tarea.final_tardio,
            self.__proyecto.num_decimales)

        # Calcula los tiempos tardíos de las otras tareas
        for nodo in reversed(list(self.__nodos.values())):
            if nodo.hijos:
                nodo.tarea.final_tardio = min(hijo.tarea.inicio_tardio for hijo in nodo.hijos)
            else:
                nodo.tarea.final_tardio = self.__tarea_final.tarea.final_tardio

            nodo.tarea.inicio_tardio = round(
                nodo.tarea.final_tardio - nodo.tarea.duracion,
                self.__proyecto.num_decimales)
            nodo.tarea.holgura = round(
                nodo.tarea.inicio_tardio - nodo.tarea.inicio_temprano,
                self.__proyecto.num_decimales)

    def __calcular_fecha_tareas(self):

        """
        Calcula las fechas de inicio y finalización de las tareas, según la unidad de tiempo definida en el proyecto.

        La fecha de inicio y finalización se calculan usando los tiempos tempranos y la duración de la tarea.
        """

        for nodo in self.__nodos.values():

            tarea = nodo.tarea

            # Convierte los tiempos tempranos a días, según la unidad de tiempo del proyecto
            if self.__proyecto.unidad_tiempo == UnidadTiempo.HORAS:
                dias_inicio_temprano = int(tarea.inicio_temprano // self.__proyecto.horas_trabajo_dia)
                dias_duracion = int(tarea.duracion // self.__proyecto.horas_trabajo_dia)
            else:
                dias_inicio_temprano = int(tarea.inicio_temprano)
                dias_duracion = int(tarea.duracion)

            # Calcula las fechas de inicio y finalización
            tarea.fecha_inicio = self.__proyecto.fecha_inicio + timedelta(days=dias_inicio_temprano)
            tarea.fecha_final = tarea.fecha_inicio + timedelta(days=dias_duracion)

    def buscar_ruta_critica(self) -> List[Tarea]:
        return [nodo.tarea
                for nodo in
                self.__nodos.values()
                if nodo.tarea.holgura == 0]

    def get_nodos(self) -> Dict[int, NodoTarea]:

        self.__tarea_inicial.tarea.proyecto = self.__proyecto
        self.__tarea_final.tarea.proyecto = self.__proyecto

        self.__nodos[self.__tarea_inicial.tarea.numero_tarea] = self.__tarea_inicial
        self.__nodos[self.__tarea_final.tarea.numero_tarea] = self.__tarea_final

        return dict(sorted(self.__nodos.items()))
