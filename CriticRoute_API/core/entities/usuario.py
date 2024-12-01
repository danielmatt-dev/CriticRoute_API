from dataclasses import dataclass


@dataclass
class Usuario:

    """
    Clase de datos para representar un usuario.

    Atributos:
        username (str): Nombre de usuario.
        email (str): Correo electrónico del usuario.
        password (str): Contraseña del usuario.
    """

    username: str
    email: str
    password: str
