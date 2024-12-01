from abc import ABC, abstractmethod


class VerificarExistenciaCorreo(ABC):

    @abstractmethod
    def execute(self, correo: str) -> bool:
        pass
