from injector import Module, singleton, provider

from CriticRoute_API.src.core.port.proyecto_repository import ProyectoRepository
from CriticRoute_API.src.core.port.repository import Repository
from CriticRoute_API.src.core.use_cases.buscar_proyecto_por_id import BuscarProyectoPorId
from CriticRoute_API.src.core.use_cases.buscar_proyectos import BuscarProyectos
from CriticRoute_API.src.core.use_cases.crear_usuario import CrearUsuario
from CriticRoute_API.src.core.use_cases.generar_cpm import GenerarCPM
from CriticRoute_API.src.core.use_cases.grafo_cpm import GrafoCPM
from CriticRoute_API.src.core.use_cases.guardar_grafo_cpm import GuardarGrafoCPM
from CriticRoute_API.src.core.use_cases.impl.buscar_proyecto_por_id_impl import BuscarProyectoPorIdImpl
from CriticRoute_API.src.core.use_cases.impl.buscar_proyectos_impl import BuscarProyectosImpl
from CriticRoute_API.src.core.use_cases.impl.crear_usuario_impl import CrearUsuarioImpl
from CriticRoute_API.src.core.use_cases.impl.generar_cpm_impl import GenerarCPMImpl
from CriticRoute_API.src.core.use_cases.impl.grafo_cpm_impl import GrafoCPMImpl
from CriticRoute_API.src.core.use_cases.impl.guardar_grafo_cpm_impl import GuardarGrafoCPMImpl
from CriticRoute_API.src.core.use_cases.impl.procesador_excel_impl import ProcesadorExcelImpl
from CriticRoute_API.src.core.use_cases.impl.verificar_existencia_correo_impl import VerificarExistenciaCorreoImpl
from CriticRoute_API.src.core.use_cases.procesador_excel import ProcesadorExcel
from CriticRoute_API.src.core.use_cases.verificar_existencia_correo import VerificarExistenciaCorreo
from CriticRoute_API.src.infraestructure.delivery.dto.mapper.mapper_dto import MapperDto
from CriticRoute_API.src.infraestructure.delivery.dto.mapper.mapper_dto_impl import MapperDtoImpl
from CriticRoute_API.src.infraestructure.persistence.adapter.adapter import Adapter
from CriticRoute_API.src.infraestructure.persistence.adapter.proyecto_adapter import ProyectoAdapter
from CriticRoute_API.src.infraestructure.persistence.mapper.mapper import Mapper
from CriticRoute_API.src.infraestructure.persistence.mapper.mapper_impl import MapperImpl


class AppModule(Module):

    """
    Módulo de configuración para la inyección de dependencias.

    Esta clase se encarga de configurar e inyectar las dependencias necesarias para
    los servicios de autenticación, como la verificación del correo, la creación de usuarios
    y el mapeo de datos.
    """

    @singleton
    @provider
    def provide_mapper(self) -> Mapper:
        """
        Proporciona una instancia del Mapper, encargado de mapear entidades a DTOs (Data Transfer Objects)
        y viceversa.

        Returns:
            Mapper: Una instancia del Mapper para la conversión entre entidades y DTOs.
        """
        return MapperImpl()

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
    def provide_proyecto_repository(self) -> ProyectoRepository:
        """
        Proporciona una implementación del repositorio para acceder y gestionar los datos relacionados
        con los proyectos.

        Returns:
            ProyectoRepository: Una instancia del repositorio para proyectos.
        """
        return ProyectoAdapter(self.provide_mapper())

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
    def provider_guardar_grafo(self) -> GuardarGrafoCPM:
        """
        Proporciona una implementación del servicio para guardar el grafo CPM de un proyecto.

        Returns:
            GuardarGrafoCPM: Una instancia del servicio para guardar el grafo CPM.
        """
        return GuardarGrafoCPMImpl(self.provide_proyecto_repository())

    @singleton
    @provider
    def provider_buscar_proyectos(self) -> BuscarProyectos:
        """
        Proveedor para BuscarProyectos. Retorna la implementación concreta BuscarProyectosImpl.

        Returns:
            BuscarProyectos: Instancia de BuscarProyectosImpl.
        """
        return BuscarProyectosImpl(self.provide_proyecto_repository())

    @singleton
    @provider
    def provider_buscar_proyecto_por_id(self) -> BuscarProyectoPorId:
        """
        Proveedor para BuscarProyectoPorId. Retorna la implementación concreta BuscarProyectoPorIdImpl.

        Returns:
            BuscarProyectoPorId: Instancia de BuscarProyectoPorIdImpl.
        """
        return BuscarProyectoPorIdImpl(self.provide_proyecto_repository())

    @singleton
    @provider
    def provider_procesador_excel(self) -> ProcesadorExcel:
        return ProcesadorExcelImpl()

    @singleton
    @provider
    def provider_grafo_cpm(self) -> GrafoCPM:
        return GrafoCPMImpl()

    @singleton
    @provider
    def provider_generar_cpm(self) -> GenerarCPM:
        return GenerarCPMImpl(self.provider_grafo_cpm(), self.provider_procesador_excel())

    @singleton
    @provider
    def provider_mapper_dto(self) -> MapperDto:
        """
        Proporciona una implementación del mapeador de datos.

        Returns:
            MapperDto: Una instancia que mapea los datos entre el serializer y las entidades.
        """
        return MapperDtoImpl()
