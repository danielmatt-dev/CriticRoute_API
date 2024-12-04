from dataclasses import dataclass
from datetime import date
from typing import Optional

from django.contrib.auth.models import User

from CriticRoute_API.src.core.entities.enums import UnidadTiempo


@dataclass
class Proyecto:

    """
    Clase que representa un proyecto. Contiene información relevante sobre el proyecto,
    como el usuario asociado, las fechas, el estado, y la unidad de tiempo utilizada.

    Atributos:
        - id_proyecto (Optional[int]): Identificador único del proyecto (opcional).
        - usuario (User): Usuario asociado al proyecto.
        - titulo (str): Título del proyecto.
        - descripcion (str): Descripción detallada del proyecto.
        - fecha_inicio (date): Fecha de inicio del proyecto.
        - unidad_tiempo (UnidadTiempo): Unidad de tiempo utilizada en el proyecto (horas o días).
        - horas_trabajo_dia (int): Número de horas de trabajo por día en el proyecto.
        - num_decimales (int): Número de decimales utilizados en los cálculos de tiempo.
        - estado (str): Estado actual del proyecto.
    """

    id_proyecto: Optional[int]
    usuario: User
    titulo: str
    descripcion: str
    fecha_inicio: date
    unidad_tiempo: UnidadTiempo
    horas_trabajo_dia: int
    num_decimales: int
    estado: str

    @classmethod
    def empty(cls, usuario: User):
        return cls(
            id_proyecto=None,
            usuario=usuario,
            titulo='',
            descripcion='',
            fecha_inicio=date(2024, 1, 1),
            unidad_tiempo=UnidadTiempo.DIAS,
            horas_trabajo_dia=0,
            num_decimales=2,
            estado='Habilitado'
        )
