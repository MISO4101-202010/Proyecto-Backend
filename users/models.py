from polymorphic.models import PolymorphicModel
# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser, PolymorphicModel):
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=255, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(null=False, auto_now=True)
    fecha_creacion = models.DateTimeField(null=False, auto_now_add=True)

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'


class Profesor(Usuario):
    facultad = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'profesor'
        verbose_name_plural = 'profesores'

    def __str__(self):
        return self.first_name + '-' + self.email


class Estudiante(Usuario):
    codigo_de_estudiante = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'estudiante'
        verbose_name_plural = 'estudiantes'

    def __str__(self):
        return str(self.first_name) + '-' + str(self.codigo_de_estudiante)
