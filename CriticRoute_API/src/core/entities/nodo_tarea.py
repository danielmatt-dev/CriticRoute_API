from typing import List

from CriticRoute_API.src.core.entities.tarea import Tarea


class NodoTarea:
    def __init__(self, tarea: Tarea):
        self.tarea = tarea
        self.padres: List[NodoTarea] = []
        self.hijos: List[NodoTarea] = []
