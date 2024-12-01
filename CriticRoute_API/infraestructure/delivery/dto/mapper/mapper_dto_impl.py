from CriticRoute_API.core.entities.usuario import Usuario
from CriticRoute_API.infraestructure.delivery.dto.mapper.mapper_dto import MapperDto
from CriticRoute_API.infraestructure.delivery.dto.response.auth_token import AuthToken


class MapperDtoImpl(MapperDto):

    def to_usuario(self, data) -> Usuario:
        return Usuario(
            email=data['email'],
            username=data['username'],
            password=data['password'],
        )

    def to_auth_token(self, token) -> AuthToken:
        return AuthToken(
            refresh=str(token),
            access=str(token.access_token)
        )
