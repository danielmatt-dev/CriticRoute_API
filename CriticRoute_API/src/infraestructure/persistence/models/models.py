from django.db import models


class TareaDependenciaModel(models.Model):
    id_tarea_dependencia = models.AutoField(primary_key=True)
    tarea_padre = models.ForeignKey('TareaModel',
                                    on_delete=models.PROTECT,
                                    db_column='id_tarea_padre',
                                    related_name="tareas_dependencias_padre")
    tarea_hijo = models.ForeignKey('TareaModel',
                                   on_delete=models.PROTECT,
                                   db_column='id_tarea_hijo',
                                   related_name="tareas_dependencias_hijo")

    class Meta:
        managed = False
        db_table = 'tareas_dependencias'


class ResponsableModel(models.Model):
    id_responsable = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'responsables'


class TareaResponsableModel(models.Model):
    id_tarea_responsable = models.AutoField(primary_key=True)
    tarea = models.ForeignKey('TareaModel',
                              on_delete=models.PROTECT,
                              db_column='id_tarea',
                              related_name="tareas_responsables")
    responsable = models.ForeignKey('ResponsableModel',
                                    on_delete=models.PROTECT,
                                    db_column='id_responsable',
                                    related_name="responsables_tareas")

    class Meta:
        managed = False
        db_table = 'tareas_responsables'
