import base64

from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from CriticRoute_API.src.core.exceptions.invalid_excel_format_ex import InvalidExcelFormatEx
from CriticRoute_API.src.core.use_cases.buscar_proyecto_por_id import BuscarProyectoPorId
from CriticRoute_API.src.core.use_cases.buscar_proyectos import BuscarProyectos
from CriticRoute_API.src.core.use_cases.generar_cpm import GenerarCPM
from CriticRoute_API.src.core.use_cases.guardar_grafo_cpm import GuardarGrafoCPM
from CriticRoute_API.src.infraestructure.delivery.dto.mapper.mapper_dto import MapperDto
from CriticRoute_API.src.infraestructure.delivery.dto.request.proyecto_serializer import ProyectoSerializer
from CriticRoute_API.src.infraestructure.delivery.dto.request.usuario_serializer import UsuarioSerializer
from CriticRoute_API.src.infraestructure.delivery.dto.response.auth_token import AuthSerializer
from CriticRoute_API.src.infraestructure.delivery.dto.response.dtos import ProyectoDTOSerializer


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def post_crear_usuario(request, verificar_usuario, crear_cuenta, mapper_dto):

    """
    Crea un usuario en el sistema y devuelve un token de autenticación.

    Este endpoint verifica si el correo ya está registrado. Si no lo está, crea
    el usuario y genera un token JWT para autenticación.

    Args:
        request (HttpRequest): La solicitud HTTP que contiene los datos del usuario.
        verificar_usuario (VerificarExistenciaCorreo): Servicio que verifica si el correo ya está registrado.
        crear_cuenta (CrearUsuario): Servicio que crea un nuevo usuario.
        mapper_dto (MapperDto): Servicio que mapea los datos del serializer a entidades y viceversa.

    Returns:
        Response: Un objeto Response que contiene el token JWT si el registro es exitoso,
                  o un error si el correo ya está registrado.
    """

    # Serializa los datos recibidos en la solicitud
    user_serializer = UsuarioSerializer(data=request.data)

    # Verifica si los datos del usuario son válidos
    if not user_serializer.is_valid():
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Verifica si el correo ya está registrado
    if verificar_usuario.execute(str(user_serializer.validated_data['email'])):
        return Response({'error': 'El correo ya esta registrado'}, status=status.HTTP_400_BAD_REQUEST)

    # Crea el usuario y obtiene el token
    token = crear_cuenta.execute(
        mapper_dto.to_usuario(user_serializer.validated_data))

    # Mapea el token a la clase AuthToken
    auth_token = mapper_dto.to_auth_token(token)
    auth_serializer = AuthSerializer(auth_token)

    # Crea la respuesta con el token y el CSRF
    response = Response(auth_serializer.data, status=status.HTTP_201_CREATED)
    response['X-CSRFToken'] = get_token(request)  # Incluye el token CSRF en la respuesta
    return response


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_nuevo_proyecto(request, generar_grafo: GenerarCPM, guardar_grafo: GuardarGrafoCPM):

    # Deserializa los datos de la solicitud
    proyecto_serializer = ProyectoSerializer(data=request.data)

    # Verifica si los datos del proyecto son válidos
    if not proyecto_serializer.is_valid():
        return Response(proyecto_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    usuario = request.user

    # Verifica si el archivo está presente en los datos de la solicitud
    if not proyecto_serializer.validated_data['file_bytes']:
        return Response({'error': 'Archivo no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    try:

        # Decodifica el archivo base64 que contiene los datos PERT
        file_byte = base64.b64decode(proyecto_serializer.validated_data['file_bytes'])

        nodos = generar_grafo.execute(
            file_bytes=file_byte,
            titulo=proyecto_serializer.validated_data['titulo'],
            descripcion=proyecto_serializer.validated_data['descripcion'],
            usuario=usuario
        )

        guardar_grafo.execute(nodos)

        return Response({'message': 'Proyecto guardado con éxito'}, status=status.HTTP_201_CREATED)

    except InvalidExcelFormatEx as ex:
        return Response({f'{ex.message}'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'Error al generar grafo'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_buscar_proyectos(request, buscar_proyectos: BuscarProyectos, mapper_dto: MapperDto):

    proyectos = buscar_proyectos.execute(request.user)
    response = mapper_dto.to_list_proyecto_dto(proyectos)
    serialized_data = ProyectoDTOSerializer(response, many=True).data

    return Response(serialized_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_buscar_proyecto_id(request, id_proyecto: int, buscar_proyecto_por_id: BuscarProyectoPorId):

    proyecto = buscar_proyecto_por_id.execute(id_proyecto, request.user)

    if proyecto is None:
        return Response({'message': 'Proyecto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProyectoDTOSerializer(proyecto).data

    return Response(serializer, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_csrf_token(request):

    """
    Devuelve el token CSRF necesario para las peticiones posteriores.

    Este endpoint es utilizado para obtener un token CSRF que se incluirá en las
    respuestas del servidor.

    Args:
        request (HttpRequest): La solicitud HTTP que solicita el token CSRF.

    Returns:
        Response: La respuesta HTTP que contiene el token CSRF.
    """

    csrf_token = get_token(request)  # Obtén el token CSRF
    return Response({'csrf_token': csrf_token})
