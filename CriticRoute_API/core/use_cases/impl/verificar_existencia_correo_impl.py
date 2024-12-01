from injector import inject

from CriticRoute_API.core.port.repository import Repository
from CriticRoute_API.core.use_cases.verificar_existencia_correo import VerificarExistenciaCorreo


# Implementación concreta del caso de uso para verificar existencia de correo.
class VerificarExistenciaCorreoImpl(VerificarExistenciaCorreo):

    @inject
    def __init__(self, repository: Repository):
        """
        Constructor de la clase que recibe una instancia del repositorio de autenticación.

        Args:
            repository (Repository): El repositorio que maneja las operaciones de la capa de persistence.
        """
        self.repository = repository

    def execute(self, correo: str) -> bool:
        return self.repository.verificar_existencia_correo(correo)
