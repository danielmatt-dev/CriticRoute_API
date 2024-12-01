from abc import ABC, abstractmethod


# Interfaz abstracta para el caso de uso de verificar existencia de un correo.
class VerificarExistenciaCorreo(ABC):

    @abstractmethod
    def execute(self, correo: str) -> bool:

        """
        Método abstracto para ejecutar la verificación de existencia de un correo.

        Args:
            correo (str): El correo electrónico a verificar.

        Returns:
            bool: Retorna True si el correo existe, False en caso contrario.
        """

        pass
