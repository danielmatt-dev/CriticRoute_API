from injector import Injector

from CriticRoute_API.core.use_cases.crear_usuario import CrearUsuario
from CriticRoute_API.core.use_cases.verificar_existencia_correo import VerificarExistenciaCorreo
from CriticRoute_API.infraestructure.delivery.dto.mapper.mapper_dto import MapperDto
from CriticRoute_API.infraestructure.delivery.views.views import post_crear_usuario
from injector_modules import AppModule


def post_crear_usuario_factory(request):
    injector = Injector([AppModule])
    verificar_existencia_usuario = injector.get(VerificarExistenciaCorreo)
    crear_usuario = injector.get(CrearUsuario)
    mapper_dto = injector.get(MapperDto)
    return post_crear_usuario(request, verificar_existencia_usuario, crear_usuario, mapper_dto)
