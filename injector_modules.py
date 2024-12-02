from injector import Module, singleton, provider

from CriticRoute_API.src.core.port.repository import Repository
from CriticRoute_API.src.core.use_cases.crear_usuario import CrearUsuario
from CriticRoute_API.src.core.use_cases.impl.crear_usuario_impl import CrearUsuarioImpl
from CriticRoute_API.src.core.use_cases.impl.verificar_existencia_correo_impl import VerificarExistenciaCorreoImpl
from CriticRoute_API.src.core.use_cases.verificar_existencia_correo import VerificarExistenciaCorreo
from CriticRoute_API.src.infraestructure.delivery.dto.mapper.mapper_dto import MapperDto
from CriticRoute_API.src.infraestructure.delivery.dto.mapper.mapper_dto_impl import MapperDtoImpl
from CriticRoute_API.src.infraestructure.persistence.adapter.adapter import Adapter


class AppModule(Module):

    """
    Módulo de configuración para la inyección de dependencias.

    Esta clase se encarga de configurar e inyectar las dependencias necesarias para
    los servicios de autenticación, como la verificación del correo, la creación de usuarios
    y el mapeo de datos.
    """

    @singleton
    @provider
    def provide_repository(self) -> Repository:
        """
        Proporciona una implementación del repositorio para acceder a los datos de los usuarios.

        Returns:
            Repository: Una instancia del repositorio que interactúa con la base de datos.
        """
        return Adapter()

    @singleton
    @provider
    def provider_verificar_usuario(self) -> VerificarExistenciaCorreo:
        """
        Proporciona una implementación del servicio para verificar la existencia de un correo.

        Returns:
            VerificarExistenciaCorreo: Una instancia del servicio que verifica si el correo ya está registrado.
        """
        return VerificarExistenciaCorreoImpl(self.provide_repository())

    @singleton
    @provider
    def provider_crear_usuario(self) -> CrearUsuario:
        """
        Proporciona una implementación del servicio para crear un nuevo usuario.

        Returns:
            CrearUsuario: Una instancia del servicio que crea usuarios en el sistema.
        """
        return CrearUsuarioImpl(self.provide_repository())

    @singleton
    @provider
    def provider_mapper_dto(self) -> MapperDto:
        """
        Proporciona una implementación del mapeador de datos.

        Returns:
            MapperDto: Una instancia que mapea los datos entre el serializer y las entidades.
        """
        return MapperDtoImpl()
