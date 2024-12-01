from injector import Module, singleton, provider

from CriticRoute_API.core.port.repository import Repository
from CriticRoute_API.core.use_cases.crear_usuario import CrearUsuario
from CriticRoute_API.core.use_cases.impl.crear_usuario_impl import CrearUsuarioImpl
from CriticRoute_API.core.use_cases.impl.verificar_existencia_correo_impl import VerificarExistenciaCorreoImpl
from CriticRoute_API.core.use_cases.verificar_existencia_correo import VerificarExistenciaCorreo
from CriticRoute_API.infraestructure.delivery.dto.mapper.mapper_dto import MapperDto
from CriticRoute_API.infraestructure.delivery.dto.mapper.mapper_dto_impl import MapperDtoImpl
from CriticRoute_API.infraestructure.persistence.adapter.adapter import Adapter


class AppModule(Module):

    @singleton
    @provider
    def provide_repository(self) -> Repository:
        return Adapter()

    @singleton
    @provider
    def provider_verificar_usuario(self) -> VerificarExistenciaCorreo:
        return VerificarExistenciaCorreoImpl(self.provide_repository())

    @singleton
    @provider
    def provider_crear_usuario(self) -> CrearUsuario:
        return CrearUsuarioImpl(self.provide_repository())

    @singleton
    @provider
    def provider_mapper_dto(self) -> MapperDto:
        return MapperDtoImpl()
