from django.contrib import admin

from activities.models import Marca, PreguntaOpcionMultiple, Opcionmultiple, PreguntaFoV, PreguntaAbierta, \
    RespuestmultipleEstudiante, RespuestaVoF, RespuestaAbiertaEstudiante, Calificacion, Pausa

# Register your models here.

models = [Marca, PreguntaOpcionMultiple, Opcionmultiple, PreguntaFoV, PreguntaAbierta,
          RespuestmultipleEstudiante, RespuestaVoF, RespuestaAbiertaEstudiante, Calificacion, Pausa]


admin.site.register(models)
