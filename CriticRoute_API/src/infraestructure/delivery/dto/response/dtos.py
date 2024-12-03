from dataclasses import dataclass
from datetime import date
from typing import Optional, List

from rest_framework import serializers


@dataclass
class ResponsableDTO:
    id_responsable: Optional[int]
    nombre: str


@dataclass
class TareaDTO:
    id_tarea: Optional[int]
    numero_tarea: int
    accion: str
    tiempo_optimista: float
    tiempo_probable: float
    tiempo_pesimista: float
    inicio_temprano: float
    duracion: float
    final_temprano: float
    inicio_tardio: float
    holgura: float
    final_tardio: float
    fecha_inicio: date
    fecha_final: date
    notas: str
    estado: str
    responsables: List[ResponsableDTO]
    tareas_dependencias: List[int]


@dataclass
class ProyectoDTO:
    id_proyecto: Optional[int]
    titulo: str
    descripcion: str
    fecha_inicio: date
    unidad_tiempo: str
    horas_trabajo_dia: int
    num_decimales: int
    estado: str
    tareas: List[TareaDTO]


class ResponsableDTOSerializer(serializers.Serializer):
    """
    Serializer para el DTO de Responsable, mapea los datos del ResponsableDTO para ser enviados o recibidos en la API.
    """
    id_responsable = serializers.IntegerField(required=False)
    nombre = serializers.CharField(max_length=100)


class TareaDTOSerializer(serializers.Serializer):
    """
    Serializer para el DTO de Tarea, mapea los datos del TareaDTO para ser enviados o recibidos en la API.
    """
    id_tarea = serializers.IntegerField(required=False)
    numero_tarea = serializers.IntegerField()
    accion = serializers.CharField(max_length=255)
    tiempo_optimista = serializers.FloatField()
    tiempo_probable = serializers.FloatField()
    tiempo_pesimista = serializers.FloatField()
    inicio_temprano = serializers.FloatField()
    duracion = serializers.FloatField()
    final_temprano = serializers.FloatField()
    inicio_tardio = serializers.FloatField()
    holgura = serializers.FloatField()
    final_tardio = serializers.FloatField()
    fecha_inicio = serializers.DateField()
    fecha_final = serializers.DateField()
    notas = serializers.CharField(max_length=1000)
    estado = serializers.CharField(max_length=20)
    responsables = ResponsableDTOSerializer(many=True)
    tareas_dependencias = serializers.ListField(child=serializers.IntegerField())


class ProyectoDTOSerializer(serializers.Serializer):
    """
    Serializer para el DTO de Proyecto, mapea los datos del ProyectoDTO para ser enviados o recibidos en la API.
    """
    id_proyecto = serializers.IntegerField(required=False)
    titulo = serializers.CharField(max_length=50)
    descripcion = serializers.CharField(max_length=255)
    fecha_inicio = serializers.DateField()
    unidad_tiempo = serializers.CharField(max_length=5)
    horas_trabajo_dia = serializers.IntegerField()
    num_decimales = serializers.IntegerField(default=2)
    estado = serializers.CharField(max_length=20)
    tareas = TareaDTOSerializer(many=True, required=False)
