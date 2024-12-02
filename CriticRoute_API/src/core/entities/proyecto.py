from dataclasses import dataclass
from datetime import date
from typing import Optional

from CriticRoute_API.src.core.entities.enums import UnidadTiempo
from CriticRoute_API.src.core.entities.usuario import Usuario


@dataclass
class Proyecto:

    """
    Clase que representa un proyecto. Contiene información relevante sobre el proyecto,
    como el usuario asociado, las fechas, el estado, y la unidad de tiempo utilizada.

    Atributos:
        - id_proyecto (Optional[int]): Identificador único del proyecto (opcional).
        - usuario (Usuario): Usuario asociado al proyecto.
        - titulo (str): Título del proyecto.
        - descripcion (str): Descripción detallada del proyecto.
        - fecha_inicio (date): Fecha de inicio del proyecto.
        - unidad_tiempo (UnidadTiempo): Unidad de tiempo utilizada en el proyecto (horas o días).
        - horas_trabajo_dia (int): Número de horas de trabajo por día en el proyecto.
        - num_decimales (int): Número de decimales utilizados en los cálculos de tiempo.
        - estado (str): Estado actual del proyecto.
    """

    id_proyecto: Optional[int]
    usuario: Usuario
    titulo: str
    descripcion: str
    fecha_inicio: date
    unidad_tiempo: UnidadTiempo
    horas_trabajo_dia: int
    num_decimales: int
    estado: str
