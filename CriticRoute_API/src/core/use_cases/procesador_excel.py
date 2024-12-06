from abc import ABC, abstractmethod
from typing import Optional, Dict, List, Any


class ProcesadorExcel(ABC):

    @abstractmethod
    def get_file_bytes(self) -> Optional[bytes]:
        """
        Devuelve los bytes del archivo Excel almacenados en el procesador.

        Returns:
            Optional[bytes]: Los bytes del archivo Excel, o None si no se ha cargado un archivo.
        """
        pass

    @abstractmethod
    def set_file_bytes(self, file_bytes: bytes):
        """
        Establece los bytes del archivo Excel a procesar. Al establecer los bytes, también
        limpia y renombra las columnas del DataFrame extraído.

        Args:
            file_bytes (bytes): Los bytes del archivo Excel que se deben procesar.
        """
        pass

    @abstractmethod
    def extraer_datos_proyecto(self) -> Dict[str, Any]:
        """
        Extrae los datos de configuración del proyecto desde el archivo Excel.

        Returns:
            Dict[str, Any]: Un diccionario con los datos extraídos, como fecha de inicio, unidad de tiempo, etc.
        """
        pass

    @abstractmethod
    def procesar_datos_actividades(self) -> List[Dict]:
        """
        Procesa los datos de las actividades contenidas en el DataFrame del archivo Excel.

        Itera sobre cada fila y construye un diccionario con la información relevante de cada actividad.

        Returns:
            List[Dict]: Una lista de diccionarios donde cada diccionario contiene los datos de una actividad.
        """
        pass
