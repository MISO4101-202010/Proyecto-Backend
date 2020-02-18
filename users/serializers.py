from rest_framework import serializers
from users.models import Profesor, Estudiante
from interactive_content.serializers import CursoSerializer


class ProfesorSerializer(serializers.ModelSerializer):
    cursos = CursoSerializer(many=True, read_only=True)

    class Meta:
        model = Profesor
        fields = ('username', 'first_name', 'last_name', 'email', 'direccion', 'telefono', 'facultad', 'cursos')


class EstudianteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Estudiante
        fields = '__all__'
