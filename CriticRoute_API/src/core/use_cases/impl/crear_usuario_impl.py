from injector import inject
from rest_framework_simplejwt.tokens import Token

from CriticRoute_API.src.core.entities.usuario import Usuario
from CriticRoute_API.src.core.port.repository import Repository
from CriticRoute_API.src.core.use_cases.crear_usuario import CrearUsuario


# Implementación concreta del caso de uso para crear un usuario.
class CrearUsuarioImpl(CrearUsuario):

    @inject
    def __init__(self, repository: Repository):
        """
        Constructor de la clase que recibe una instancia del repositorio de autenticación.

        Args:
            repository (Repository): El repositorio que maneja las operaciones de la capa de persistence.
        """
        self.repository = repository

    def execute(self, usuario: Usuario) -> Token:
        return self.repository.crear_usuario(usuario)
