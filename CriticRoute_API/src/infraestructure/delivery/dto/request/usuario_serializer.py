from django.core.validators import RegexValidator, EmailValidator
from rest_framework import serializers


class UsuarioSerializer(serializers.Serializer):

    """
    Serializador para la validación y deserialización de los datos del usuario.

    Esta clase define las reglas para validar los campos como el correo, el nombre
    de usuario y la contraseña, asegurando que cumplan con los requisitos establecidos.
    """

    username = serializers.CharField(
        min_length=5,
        max_length=150,
        error_messages={
            'min_length': 'El usuario debe tener al menos 5 caracteres',
            'max_length': 'El usuario no puede tener más de 150 caracteres',
            'required': 'El usuario es obligatorio',
        }
    )

    password = serializers.CharField(
        min_length=0,
        max_length=128,
        validators=[
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$',
                message='La contraseña debe tener al menos 8 caracteres, incluyendo al menos una letra mayúscula, '
                        'una letra minúscula y un número'
            )
        ]
    )

    email = serializers.EmailField(
        min_length=0,
        max_length=254,
        validators=[
            EmailValidator(
                message='Introduce una dirección de correo electrónico válida'
            )
        ]
    )
