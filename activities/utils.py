from activities.models import Actividad
from django.db import models

def get_total_qualifying_questions(contenido):
      return Actividad.objects.filter(marca__contenido=contenido).filter(
            models.Q(preguntafov__isnull=False) |
            models.Q(preguntaopcionmultiple__isnull=False)
        ).count()
