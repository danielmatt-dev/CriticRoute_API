from abc import ABC, abstractmethod
from typing import Optional, Dict, List, Any


class ProcesadorExcel(ABC):

    @abstractmethod
    def get_file_bytes(self) -> Optional[bytes]:
        pass

    @abstractmethod
    def set_file_bytes(self, file_bytes: bytes):
        pass

    @abstractmethod
    def extraer_datos_proyecto(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def procesar_datos_actividades(self) -> List[Dict]:
        pass
