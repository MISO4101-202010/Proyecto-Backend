from django.contrib import admin

# Register your models here.
from interactive_content.models import Curso, Contenido, ContenidoInteractivo, Grupo

Models = [Curso, Contenido, ContenidoInteractivo, Grupo]

admin.site.register(Models)
