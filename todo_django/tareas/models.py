from django.db import models
from django.utils import timezone


class Prioridad(models.IntegerChoices):
    BAJA = 1, 'Baja'
    MEDIA = 2, 'Media'
    ALTA = 3, 'Alta'


class Tarea(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, default='')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_limite = models.DateField(null=True, blank=True)
    prioridad = models.IntegerField(
        choices=Prioridad.choices,
        default=Prioridad.MEDIA
    )
    etiquetas = models.CharField(max_length=200, blank=True, default='')
    completada = models.BooleanField(default=False)

    class Meta:
        ordering = ['-prioridad', 'fecha_limite']
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'

    def __str__(self):
        return self.titulo

    def get_prioridad_display_class(self):
        clases = {
            1: 'priority-low',
            2: 'priority-medium',
            3: 'priority-high'
        }
        return clases.get(self.prioridad, 'priority-medium')

    def get_prioridad_badge_class(self):
        clases = {
            1: 'badge-low',
            2: 'badge-medium',
            3: 'badge-high'
        }
        return clases.get(self.prioridad, 'badge-medium')

    def get_etiquetas_list(self):
        if self.etiquetas:
            return [e.strip() for e in self.etiquetas.split(',')]
        return []

    def get_prioridad_nombre(self):
        nombres = {
            1: 'Baja',
            2: 'Media',
            3: 'Alta'
        }
        return nombres.get(self.prioridad, 'Media')
