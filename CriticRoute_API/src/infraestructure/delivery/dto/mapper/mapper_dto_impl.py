from typing import List

from CriticRoute_API.src.core.entities.proyecto import Proyecto
from CriticRoute_API.src.core.entities.usuario import Usuario
from CriticRoute_API.src.infraestructure.delivery.dto.mapper.mapper_dto import MapperDto
from CriticRoute_API.src.infraestructure.delivery.dto.response.auth_token import AuthToken
from CriticRoute_API.src.infraestructure.delivery.dto.response.dtos import ProyectoDTO


class MapperDtoImpl(MapperDto):

    """
    Implementación de la interfaz MapperDto.

    Esta clase proporciona la implementación concreta de los métodos para convertir
    los datos del serializer a objetos de entidad y crear tokens de autenticación.
    """

    def to_list_proyecto_dto(self, proyectos: List[Proyecto]) -> List[ProyectoDTO]:
        return [self.to_proyecto_dto(proyecto) for proyecto in proyectos]

    def to_proyecto_dto(self, proyecto: Proyecto) -> ProyectoDTO:
        return ProyectoDTO(
            id_proyecto=proyecto.id_proyecto,
            titulo=proyecto.titulo,
            descripcion=proyecto.descripcion,
            fecha_inicio=proyecto.fecha_inicio,
            unidad_tiempo=proyecto.unidad_tiempo.value,
            horas_trabajo_dia=proyecto.horas_trabajo_dia,
            num_decimales=proyecto.num_decimales,
            estado=proyecto.estado,
            tareas=[]
        )

    def to_usuario(self, data) -> Usuario:
        return Usuario(
            id_usuario=data['id_usuario'],
            email=data['email'],
            username=data['username'],
            password=data['password'],
        )

    def to_auth_token(self, token) -> AuthToken:
        return AuthToken(
            refresh=str(token),
            access=str(token.access_token)
        )
