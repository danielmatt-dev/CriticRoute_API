from injector import inject
from rest_framework_simplejwt.tokens import Token

from CriticRoute_API.core.port.repository import Repository
from CriticRoute_API.core.use_cases.crear_usuario import CrearUsuario


class CrearUsuarioImpl(CrearUsuario):

    @inject
    def __init__(self, repository: Repository):
        self.repository = repository

    def execute(self, usuario) -> Token:
        return self.repository.crear_usuario(usuario)
