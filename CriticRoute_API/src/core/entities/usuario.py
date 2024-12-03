from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:

    """
    Clase de datos para representar un usuario.

    Atributos:
        username (str): Nombre de usuario.
        email (str): Correo electrónico del usuario.
        password (str): Contraseña del usuario.
    """

    id_usuario: Optional[int]
    username: str
    email: str
    password: str
