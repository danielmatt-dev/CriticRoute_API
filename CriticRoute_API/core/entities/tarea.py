from dataclasses import dataclass
from datetime import date
from typing import Optional

from CriticRoute_API.core.entities.enums import Estado
from CriticRoute_API.core.entities.proyecto import Proyecto


@dataclass
class Tarea:

    """
    Clase que representa una tarea dentro de un proyecto. Contiene información sobre la tarea,
    como la duración, los tiempos optimista, probable y pesimista, y su estado.

    Atributos:
        - id_tarea (Optional[int]): Identificador único de la tarea (opcional).
        - numero_tarea (int): Número que identifica de manera única a la tarea dentro del proyecto.
        - proyecto (Optional[Proyecto]): Proyecto al que pertenece la tarea.
        - accion (str): Descripción breve de la tarea a realizar.
        - descripcion (str): Descripción detallada de la tarea.
        - tiempo_optimista (float): Estimación optimista del tiempo para la tarea.
        - tiempo_probable (float): Estimación probable del tiempo para la tarea.
        - tiempo_pesimista (float): Estimación pesimista del tiempo para la tarea.
        - inicio_temprano (float): Fecha de inicio temprana calculada para la tarea.
        - duracion (float): Duración total de la tarea.
        - final_temprano (float): Fecha de finalización temprana calculada para la tarea.
        - inicio_tardio (float): Fecha de inicio tardío calculada para la tarea.
        - holgura (float): Tiempo de holgura calculado para la tarea.
        - final_tardio (float): Fecha de finalización tardía calculada para la tarea.
        - fecha_inicio (date): Fecha en la que realmente se inicia la tarea.
        - fecha_final (date): Fecha en la que se finaliza la tarea.
        - estado (Estado): Estado actual de la tarea (por iniciar, en progreso, terminado).
    """

    id_tarea: Optional[int]
    numero_tarea: int
    proyecto: Optional[Proyecto]
    accion: str
    descripcion: str
    tiempo_optimista: float
    tiempo_probable: float
    tiempo_pesimista: float
    inicio_temprano: float
    duracion: float
    final_temprano: float
    inicio_tardio: float
    holgura: float
    final_tardio: float
    fecha_inicio: date
    fecha_final: date
    estado: Estado

    @classmethod
    def from_basic(
            cls,
            numero_tarea: int,
            proyecto: Proyecto,
            accion: str,
            tiempo_optimista: float,
            tiempo_probable: float,
            tiempo_pesimista: float,
            descripcion: str
    ):
        """
        Método de clase para crear una instancia de la tarea con parámetros básicos.

        Args:
            - numero_tarea (int): Número que identifica a la tarea.
            - proyecto (Proyecto): Proyecto al que pertenece la tarea.
            - accion (str): Descripción breve de la tarea.
            - tiempo_optimista (float): Estimación optimista del tiempo para la tarea.
            - tiempo_probable (float): Estimación probable del tiempo para la tarea.
            - tiempo_pesimista (float): Estimación pesimista del tiempo para la tarea.
            - descripcion (str): Descripción detallada de la tarea.

        Returns:
            Tarea: Instancia de la clase Tarea con los atributos configurados.
        """

        return cls(
            id_tarea=None,
            numero_tarea=numero_tarea,
            proyecto=proyecto,
            accion=accion,
            tiempo_optimista=tiempo_optimista,
            tiempo_probable=tiempo_probable,
            tiempo_pesimista=tiempo_pesimista,
            inicio_temprano=0.0,
            duracion=0.0,
            final_temprano=0.0,
            inicio_tardio=0.0,
            holgura=0.0,
            final_tardio=0.0,
            fecha_inicio=date(2024, 1, 1),
            fecha_final=date(2024, 1, 1),
            descripcion=descripcion,
            estado=Estado.POR_INICIAR
        )

    @classmethod
    def empty(cls):

        """
        Método de clase que crea una tarea vacía con valores predeterminados.

        Returns:
            Tarea: Instancia de la clase Tarea con valores por defecto.
        """

        return cls(
            id_tarea=None,
            numero_tarea=0,
            proyecto=None,
            accion='',
            tiempo_optimista=0.0,
            tiempo_probable=0.0,
            tiempo_pesimista=0.0,
            inicio_temprano=0.0,
            duracion=0.0,
            final_temprano=0.0,
            inicio_tardio=0.0,
            holgura=0.0,
            final_tardio=0.0,
            fecha_inicio=date(2024, 1, 1),
            fecha_final=date(2024, 1, 1),
            descripcion='',
            estado=Estado.POR_INICIAR
        )

    def calcular_duracion(self, num_decimales: int):

        """
        Método para calcular la duración de la tarea utilizando la fórmula de PERT.

        Args:
            num_decimales (int): Número de decimales para redondear el resultado.

        Returns:
            duracion (float): El valor del atributo `duracion` de la tarea.
        """

        self.duracion = (
            round(((self.tiempo_optimista + 4 * self.tiempo_probable + self.tiempo_pesimista) / 6), num_decimales))
