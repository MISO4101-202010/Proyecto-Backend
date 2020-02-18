from django.db import models

# Create your models here.
from users.models import Profesor, Estudiante


class Curso(models.Model):
    fecha_creacion = models.DateTimeField(null=False, auto_now_add=True)
    nombre = models.CharField(max_length=255, blank=False, null=False)
    profesor = models.ForeignKey(Profesor, blank=False, null=False, on_delete=models.CASCADE, related_name="cursos")
    descripcion = models.TextField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.nombre


class Contenido(models.Model):
    url = models.CharField(max_length=255, blank=False, null=False)
    nombre = models.CharField(max_length=255, blank=False, null=False)
    profesor = models.ForeignKey(Profesor, blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class ContenidoInteractivo(models.Model):
    nombre = models.CharField(max_length=255, blank=False, null=False)
    contenido = models.ForeignKey(Contenido, blank=False, null=False, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(null=False, auto_now_add=True)
    tiempo_disponibilidad = models.DateTimeField(null=True, blank=True)
    tiene_retroalimentacion = models.BooleanField(null=True, blank=True)
    curso = models.ManyToManyField(Curso)

    class Meta:
        verbose_name = 'contenido interactivo'
        verbose_name_plural = 'contenidos interactivos'

    def __str__(self):
        return self.contenido.nombre + '-' + str(self.fecha_creacion)


class Grupo(models.Model):
    curso = models.ForeignKey(Curso, blank=False, null=False, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.curso.nombre


