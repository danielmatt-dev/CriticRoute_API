from injector import Injector
from rest_framework.response import Response

from CriticRoute_API.src.core.use_cases.buscar_proyecto_por_id import BuscarProyectoPorId
from CriticRoute_API.src.core.use_cases.buscar_proyectos import BuscarProyectos
from CriticRoute_API.src.core.use_cases.crear_usuario import CrearUsuario
from CriticRoute_API.src.core.use_cases.generar_cpm import GenerarCPM
from CriticRoute_API.src.core.use_cases.guardar_grafo_cpm import GuardarGrafoCPM
from CriticRoute_API.src.core.use_cases.verificar_existencia_correo import VerificarExistenciaCorreo
from CriticRoute_API.src.infraestructure.delivery.dto.mapper.mapper_dto import MapperDto
from CriticRoute_API.src.infraestructure.delivery.views.views import post_crear_usuario, get_buscar_proyectos, \
    get_buscar_proyecto_id, post_nuevo_proyecto
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


def post_nuevo_proyecto_factory(request) -> Response:
    """
    Crea un nuevo proyecto en el sistema utilizando la inyección de dependencias.

    Este método inyecta las dependencias necesarias para generar el grafo CPM y luego guardar el proyecto.

    Args:
        request (HttpRequest): La solicitud HTTP que contiene los datos del proyecto a crear.

    Returns:
        Response: Una respuesta HTTP que indica el resultado de la operación de creación del proyecto.
    """
    injector = Injector([AppModule])
    generar_grafo = injector.get(GenerarCPM)
    guardar_grafo = injector.get(GuardarGrafoCPM)

    return post_nuevo_proyecto(request, generar_grafo, guardar_grafo)


def get_buscar_proyectos_factory(request) -> Response:
    """
    Busca los proyectos del usuario autenticado utilizando la inyección de dependencias.

    Este método inyecta las dependencias necesarias para buscar proyectos y mapear los resultados a DTOs.

    Args:
        request (HttpRequest): La solicitud HTTP que realiza la búsqueda de los proyectos.

    Returns:
        Response: Una respuesta HTTP con la lista de proyectos del usuario en formato DTO.
    """
    injector = Injector([AppModule])
    buscar_proyectos = injector.get(BuscarProyectos)
    mapper_dto = injector.get(MapperDto)

    return get_buscar_proyectos(request, buscar_proyectos, mapper_dto)


def get_buscar_proyecto_id_factory(request, id_proyecto) -> Response:
    """
    Busca un proyecto por su ID utilizando la inyección de dependencias.

    Este método inyecta la dependencia necesaria para buscar un proyecto por su ID.

    Args:
        request (HttpRequest): La solicitud HTTP que solicita un proyecto específico.
        id_proyecto (int): El ID del proyecto a buscar.

    Returns:
        Response: Una respuesta HTTP que contiene los detalles del proyecto encontrado o un mensaje de error.
    """
    injector = Injector([AppModule])
    buscar_proyecto_por_id = injector.get(BuscarProyectoPorId)

    return get_buscar_proyecto_id(request, id_proyecto, buscar_proyecto_por_id)
