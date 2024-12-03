from django.contrib.auth.models import User
from django.db import models

from CriticRoute_API.src.core.entities.enums import UnidadTiempo


class ProyectoModel(models.Model):
    id_proyecto = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User,
                                on_delete=models.PROTECT,
                                db_column='id_usuario',
                                related_name="proyectos")
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=255)
    fecha_inicio = models.DateField()
    unidad_tiempo = models.CharField(
        max_length=5,
        choices=[(tag, tag.value) for tag in UnidadTiempo],
    )
    horas_trabajo_dia = models.IntegerField()
    num_decimales = models.IntegerField(default=2)
    estado = models.CharField(max_length=100)

    class Meta:
        db_table = 'proyectos'
        managed = False
