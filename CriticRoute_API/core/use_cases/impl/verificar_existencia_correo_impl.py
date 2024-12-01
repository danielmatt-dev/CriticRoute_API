from injector import inject

from CriticRoute_API.core.port.repository import Repository
from CriticRoute_API.core.use_cases.verificar_existencia_correo import VerificarExistenciaCorreo


class VerificarExistenciaCorreoImpl(VerificarExistenciaCorreo):

    @inject
    def __init__(self, repository: Repository):
        self.repository = repository

    def execute(self, correo: str) -> bool:
        return self.repository.verificar_existencia_correo(correo)
