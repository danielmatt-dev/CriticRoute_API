from dataclasses import dataclass


@dataclass
class Usuario:
    username: str
    email: str
    password: str
