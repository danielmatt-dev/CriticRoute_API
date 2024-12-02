from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from CriticRoute_API.src.infraestructure.delivery.dto.request.usuario_serializer import UsuarioSerializer
from CriticRoute_API.src.infraestructure.delivery.dto.response.auth_token import AuthSerializer


@ensure_csrf_cookie
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
