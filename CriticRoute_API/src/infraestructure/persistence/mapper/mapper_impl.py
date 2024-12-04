from typing import List

from django.contrib.auth.models import User

from CriticRoute_API.src.core.entities.enums import UnidadTiempo, Estado
from CriticRoute_API.src.core.entities.proyecto import Proyecto
from CriticRoute_API.src.core.entities.tarea import Tarea, TareaDependencia, Responsable, TareaResponsable
from CriticRoute_API.src.core.entities.usuario import Usuario
from CriticRoute_API.src.infraestructure.persistence.mapper.mapper import Mapper
from CriticRoute_API.src.infraestructure.persistence.models.models import TareaResponsableModel, ResponsableModel, \
    TareaDependenciaModel
from CriticRoute_API.src.infraestructure.persistence.models.proyecto_model import ProyectoModel
from CriticRoute_API.src.infraestructure.persistence.models.tarea_model import TareaModel


class MapperImpl(Mapper):

    def to_usuario(self, model: User) -> Usuario:
        return Usuario(
            id_usuario=None,
            username=model.username,
            email=model.email,
            password=model.password
        )

    def to_usuario_model(self, entity: Usuario) -> User:
        return User(
            username=entity.username,
            email=entity.email,
            password=entity.password
        )

    def to_proyecto(self, model: ProyectoModel) -> Proyecto:
        return Proyecto(
            id_proyecto=model.id_proyecto,
            usuario=model.usuario,
            titulo=model.titulo,
            descripcion=model.descripcion,
            fecha_inicio=model.fecha_inicio,
            unidad_tiempo=UnidadTiempo(model.unidad_tiempo),
            horas_trabajo_dia=model.horas_trabajo_dia,
            num_decimales=model.num_decimales,
            estado=model.estado
        )

    def to_proyecto_model(self, entity: Proyecto) -> ProyectoModel:
        return ProyectoModel(
            usuario=entity.usuario,
            titulo=entity.titulo,
            descripcion=entity.descripcion,
            fecha_inicio=entity.fecha_inicio,
            unidad_tiempo=entity.unidad_tiempo.value,
            horas_trabajo_dia=entity.horas_trabajo_dia,
            num_decimales=entity.num_decimales,
            estado=entity.estado
        )

    def to_tarea(self, model: TareaModel) -> Tarea:
        return Tarea(
            id_tarea=model.id_tarea,
            numero_tarea=model.numero_tarea,
            proyecto=self.to_proyecto(model.proyecto),
            accion=model.accion,
            descripcion=model.descripcion,
            tiempo_optimista=model.tiempo_optimista,
            tiempo_probable=model.tiempo_probable,
            tiempo_pesimista=model.tiempo_pesimista,
            inicio_temprano=model.inicio_temprano,
            duracion=model.duracion,
            final_temprano=model.final_temprano,
            inicio_tardio=model.inicio_tardio,
            holgura=model.holgura,
            final_tardio=model.final_tardio,
            fecha_inicio=model.fecha_inicio,
            fecha_final=model.fecha_final,
            estado=Estado(model.estado),
            responsables=[]
        )

    def to_tarea_model(self, entity: Tarea) -> TareaModel:
        return TareaModel(
            numero_tarea=entity.numero_tarea,
            proyecto=self.to_proyecto_model(entity.proyecto),
            accion=entity.accion,
            descripcion=entity.descripcion,
            tiempo_optimista=entity.tiempo_optimista,
            tiempo_probable=entity.tiempo_probable,
            tiempo_pesimista=entity.tiempo_pesimista,
            inicio_temprano=entity.inicio_temprano,
            duracion=entity.duracion,
            final_temprano=entity.final_temprano,
            inicio_tardio=entity.inicio_tardio,
            holgura=entity.holgura,
            final_tardio=entity.final_tardio,
            fecha_inicio=entity.fecha_inicio,
            fecha_final=entity.fecha_final,
            estado=entity.estado.value
        )

    def to_list_tarea_model(self, entities: List[Tarea]) -> List[TareaModel]:
        return [self.to_tarea_model(entity) for entity in entities]

    def to_list_tarea(self, models: List[TareaModel]) -> List[Tarea]:
        return [self.to_tarea(tarea) for tarea in models]

    def to_tarea_dependencia(self, model: TareaDependenciaModel) -> TareaDependencia:
        return TareaDependencia(
            id_tarea_dependencia=model.id_tarea_dependencia,
            tarea_padre=self.to_tarea(model.tarea_padre),
            tarea_hijo=self.to_tarea(model.tarea_hijo)
        )

    def to_tarea_dependencia_model(self, entity: TareaDependencia) -> TareaDependenciaModel:
        return TareaDependenciaModel(
            tarea_padre=self.to_tarea_model(entity.tarea_padre),
            tarea_hijo=self.to_tarea_model(entity.tarea_hijo)
        )

    def to_responsable(self, model: ResponsableModel) -> Responsable:
        return Responsable(
            id_responsable=model.id_responsable,
            nombre=model.nombre
        )

    def to_responsable_model(self, entity: Responsable) -> ResponsableModel:
        return ResponsableModel(
            nombre=entity.nombre
        )

    def to_tarea_responsable(self, model: TareaResponsableModel) -> TareaResponsable:
        return TareaResponsable(
            id_tarea_responsable=model.id_tarea_responsable,
            tarea=self.to_tarea(model.tarea),
            responsable=self.to_responsable(model.responsable)
        )

    def to_tarea_responsable_model(self, entity: TareaResponsable) -> TareaResponsableModel:
        return TareaResponsableModel(
            tarea=self.to_tarea_model(entity.tarea),
            responsable=self.to_responsable_model(entity.responsable)
        )

    def to_list_tarea_dependencia(self, models: List[TareaDependenciaModel]) -> List[TareaDependencia]:
        return [self.to_tarea_dependencia(tarea) for tarea in models]

    def to_list_tarea_dependencia_model(self, entities: List[TareaDependencia]) -> List[TareaDependenciaModel]:
        return [self.to_tarea_dependencia_model(entity) for entity in entities]

    def to_list_responsable(self, models: List[ResponsableModel]) -> List[Responsable]:
        return [self.to_responsable(responsable) for responsable in models]

    def to_list_responsable_model(self, entities: List[Responsable]) -> List[ResponsableModel]:
        return [self.to_responsable_model(entity) for entity in entities]

    def to_list_tarea_responsable(self, models: List[TareaResponsableModel]) -> List[TareaResponsable]:
        return [self.to_tarea_responsable(responsable) for responsable in models]

    def to_list_tarea_responsable_model(self, entities: List[TareaResponsable]) -> List[TareaResponsableModel]:
        return [self.to_tarea_responsable_model(entity) for entity in entities]

    def to_list_proyecto(self, models: List[ProyectoModel]) -> List[Proyecto]:
        return [self.to_proyecto(proyecto) for proyecto in models]

    def to_list_proyecto_model(self, entities: List[Proyecto]) -> List[ProyectoModel]:
        return [self.to_proyecto_model(entity) for entity in entities]
