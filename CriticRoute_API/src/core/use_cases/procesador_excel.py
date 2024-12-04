from abc import ABC, abstractmethod
from typing import Optional, Dict, List

from CriticRoute_API.src.core.entities.proyecto import Proyecto


class ProcesadorExcel(ABC):
    """
    Clase abstracta que define las operaciones necesarias para procesar la plantilla en Excel
    relacionado con la gestión de proyectos y actividades.
    """

    @abstractmethod
    def get_file_bytes(self) -> Optional[bytes]:
        """Obtiene los bytes del archivo Excel."""
        pass

    @abstractmethod
    def set_file_bytes(self, file_bytes: bytes):
        """Establece los bytes del archivo Excel y procesa las columnas relevantes."""
        pass

    @abstractmethod
    def extraer_datos_proyecto(self) -> Proyecto:
        """
        Extrae los datos de configuración del proyecto, como la fecha de inicio, la unidad de tiempo,
        las horas de trabajo al día y el número de decimales, desde el archivo Excel.
        """
        pass

    @abstractmethod
    def procesar_datos_actividades(self) -> List[Dict]:
        """
        Procesa los datos de actividades contenidos en el DataFrame. Cada fila es transformada
        en un diccionario con los detalles de la actividad.
        """
        pass
