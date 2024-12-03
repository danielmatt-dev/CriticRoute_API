from datetime import date

from django.db import models

from CriticRoute_API.src.core.entities.enums import Estado
from CriticRoute_API.src.infraestructure.persistence.models.proyecto_model import ProyectoModel


class TareaModel(models.Model):
    id_tarea = models.AutoField(primary_key=True)
    numero_tarea = models.IntegerField()
    proyecto = models.ForeignKey(ProyectoModel, on_delete=models.PROTECT)
    accion = models.CharField(max_length=255)
    descripcion = models.TextField()
    tiempo_optimista = models.FloatField()
    tiempo_probable = models.FloatField()
    tiempo_pesimista = models.FloatField()
    inicio_temprano = models.FloatField()
    duracion = models.FloatField()
    final_temprano = models.FloatField()
    inicio_tardio = models.FloatField()
    holgura = models.FloatField()
    final_tardio = models.FloatField()
    fecha_inicio = models.DateField(default=date.today)
    fecha_final = models.DateField(default=date.today)
    estado = models.CharField(
        max_length=20,
        choices=[(tag, tag.value) for tag in Estado],
    )

    class Meta:
        db_table = 'tareas'
        managed = False
