from dataclasses import dataclass

from rest_framework import serializers


@dataclass
class AuthToken:

    """
    Esta clase se utiliza para almacenar los tokens de acceso y refresco que se generan
    durante el proceso de autenticación.
    """

    refresh: str
    access: str


class AuthSerializer(serializers.Serializer):

    """
    Serializador para los tokens de autenticación.

    Esta clase se encarga de serializar el objeto AuthToken para ser enviado en las respuestas
    a los usuarios que han sido autenticados.
    """

    refresh = serializers.CharField()
    access = serializers.CharField()
