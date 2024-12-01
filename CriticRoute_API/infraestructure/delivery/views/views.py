from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from CriticRoute_API.infraestructure.delivery.dto.request.usuario_serializer import UsuarioSerializer
from CriticRoute_API.infraestructure.delivery.dto.response.auth_token import AuthSerializer


@ensure_csrf_cookie
@api_view(['POST'])
@permission_classes([AllowAny])
def post_crear_usuario(request, verificar_usuario, crear_cuenta, mapper_dto):
    user_serializer = UsuarioSerializer(data=request.data)

    if not user_serializer.is_valid():
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if verificar_usuario.execute(str(user_serializer.validated_data['email'])):
        return Response({'error': 'El correo ya esta registrado'}, status=status.HTTP_400_BAD_REQUEST)

    token = crear_cuenta.execute(
        mapper_dto.to_usuario(user_serializer.validated_data))

    auth_token = mapper_dto.to_auth_token(token)
    auth_serializer = AuthSerializer(auth_token)

    response = Response(auth_serializer.data, status=status.HTTP_201_CREATED)
    response['X-CSRFToken'] = get_token(request)  # Incluye el token CSRF en la respuesta
    return response


@api_view(['GET'])
def get_csrf_token(request):
    csrf_token = get_token(request)  # Obtén el token CSRF
    return Response({'csrf_token': csrf_token})
