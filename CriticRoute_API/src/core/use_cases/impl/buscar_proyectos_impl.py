from typing import List

from injector import inject

from CriticRoute_API.src.core.entities.proyecto import Proyecto
from CriticRoute_API.src.core.entities.usuario import Usuario
from CriticRoute_API.src.core.port.proyecto_repository import ProyectoRepository
from CriticRoute_API.src.core.use_cases.buscar_proyectos import BuscarProyectos


class BuscarProyectosImpl(BuscarProyectos):

    @inject
    def __init__(self, repository: ProyectoRepository):
        self._repository = repository

    def execute(self, usuario: Usuario) -> List[Proyecto]:
        return self._repository.buscar_proyectos(usuario)
