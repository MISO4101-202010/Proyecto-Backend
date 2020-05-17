from activities.models import Actividad
from django.db import models

def get_total_qualifying_questions(obj):
      return Actividad.objects.filter(marca__contenido=obj.preguntaVoF.marca.contenido).filter(
            models.Q(preguntafov__isnull=False) |
            models.Q(preguntaopcionmultiple__isnull=False)
        ).count()
