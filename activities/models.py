from django.db import models

from interactive_content.models import ContenidoInteractivo, Grupo
from users.models import Estudiante

# Create your models here.


class Marca(models.Model):
    nombre = models.CharField(max_length=30)
    punto = models.IntegerField(default=0)
    contenido = models.ForeignKey(
        ContenidoInteractivo, on_delete=models.CASCADE, related_name='marcas')


class Actividad(models.Model):
    nombre = models.CharField(max_length=30)
    numeroDeIntentos = models.IntegerField(default=0)
    tieneRetroalimentacion = models.BooleanField(default=False)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    retroalimentacion = models.CharField(max_length=200, null=True, blank=True)
    tipoActividad = models.IntegerField(blank=False, default=0)

    def __str__(self):
        return self.nombre


class Calificacion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    calificacion = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.calificacion)


class PreguntaOpcionMultiple(Actividad):
    enunciado = models.CharField(max_length=200, null=False)
    esMultipleResp = models.BooleanField()


class PreguntaAbierta(Actividad):
    enunciado = models.CharField(max_length=200)


class Pausa(Actividad):
    enunciado = models.CharField(max_length=1000)
    tiempo = models.FloatField(default=0)


class PreguntaFoV(Actividad):
    pregunta = models.CharField(max_length=200)
    esVerdadero = models.BooleanField()


class Respuesta(models.Model):
    fecha_creacion = models.DateTimeField(null=False, auto_now_add=True)
    intento = models.IntegerField(null=False)
    estudiante = models.ForeignKey(
        Estudiante, null=True, on_delete=models.SET_NULL)
    grupo = models.ForeignKey(Grupo, null=True, on_delete=models.SET_NULL)


class Opcionmultiple(models.Model):
    opcion = models.CharField(max_length=200)
    esCorrecta = models.BooleanField()
    preguntaSeleccionMultiple = models.ForeignKey(
        PreguntaOpcionMultiple, on_delete=models.CASCADE, related_name='opciones')


class RespuestmultipleEstudiante(Respuesta):
    respuestmultiple = models.ForeignKey(
        Opcionmultiple, null=True, on_delete=models.SET_NULL)


class RespuestaAbiertaEstudiante(Respuesta):
    respuesta = models.CharField(max_length=200)
    retroalimentacion = models.CharField(max_length=200, null=True)
    preguntaAbierta = models.ForeignKey(
        PreguntaAbierta, on_delete=models.CASCADE)

    def __str__(self):
        return self.respuesta


class RespuestaVoF(Respuesta):
    esVerdadero = models.BooleanField(default=False)
    preguntaVoF = models.ForeignKey(PreguntaFoV, on_delete=models.CASCADE)
