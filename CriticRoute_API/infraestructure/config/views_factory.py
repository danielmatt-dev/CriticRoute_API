from injector import Injector
from rest_framework.response import Response

from CriticRoute_API.core.use_cases.crear_usuario import CrearUsuario
from CriticRoute_API.core.use_cases.verificar_existencia_correo import VerificarExistenciaCorreo
from CriticRoute_API.infraestructure.delivery.dto.mapper.mapper_dto import MapperDto
from CriticRoute_API.infraestructure.delivery.views.views import post_crear_usuario
from injector_modules import AppModule


def post_crear_usuario_factory(request) -> Response:
    """
    Crea un usuario en el sistema mediante la inyección de dependencias.

    Este método se encarga de inyectar las dependencias necesarias para verificar
    la existencia del correo electrónico, crear el usuario y mapear los datos.

    Args:
        request (HttpRequest): La solicitud HTTP que contiene los datos del usuario a crear.

    Returns:
        Response: Una respuesta HTTP que contiene el token de autenticación del nuevo usuario.
    """

    injector = Injector([AppModule])
    verificar_existencia_usuario = injector.get(VerificarExistenciaCorreo)
    crear_usuario = injector.get(CrearUsuario)
    mapper_dto = injector.get(MapperDto)

    # Llama a la función principal para crear el usuario
    return post_crear_usuario(request, verificar_existencia_usuario, crear_usuario, mapper_dto)
