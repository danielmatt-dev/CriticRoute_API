from enum import Enum


class UnidadTiempo(Enum):
    """
    Enum que representa las unidades de tiempo utilizadas en el proyecto.

    Las opciones disponibles son:
        - HORAS: Representa la unidad de tiempo en horas.
        - DIAS: Representa la unidad de tiempo en días.
    """
    HORAS = 'Horas'
    DIAS = 'Dias'


class Estado(Enum):
    """
    Enum que representa los posibles estados de una tarea dentro de un proyecto.

    Los estados posibles son:
        - POR_INICIAR: La tarea aún no ha comenzado.
        - EN_PROGRESO: La tarea está siendo ejecutada.
        - TERMINADO: La tarea ha sido completada.
    """
    POR_INICIAR = 'Pendiente'
    EN_PROGRESO = 'En progreso'
    TERMINADO = 'Completada'
