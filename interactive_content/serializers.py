from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from activities.serializers import MarcaSerializer
from interactive_content.models import Contenido, Curso, ContenidoInteractivo, Grupo
from users.models import Estudiante


class ContenidoSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField()
    url = serializers.URLField()

    class Meta:
        model = Contenido
        fields = ('id', 'nombre', 'url')


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'


class ContenidoInteractivoSerializer(serializers.ModelSerializer):
    cursos = SerializerMethodField('get_serialized_classes')
    contenido = ContenidoSerializer(read_only=True)
    marcas = MarcaSerializer(read_only=True, many=True)

    class Meta:
        model = ContenidoInteractivo
        fields = '__all__'

    def get_serialized_classes(self, obj):
        return CursoSerializer(obj.curso.all(), many=True).data


class ContenidoInteractivoFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContenidoInteractivo
        fields = '__all__'


class ContenidoInteractivoDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContenidoInteractivo
        fields = ['id', 'nombre']


class EstudianteDetailsSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()

    @staticmethod
    def get_nombre_completo(obj):
        return str.capitalize(obj.first_name) + ' ' + str.capitalize(obj.last_name)

    class Meta:
        model = Estudiante
        fields = ('codigo_de_estudiante', 'nombre_completo')


class CursoDetailsSerializer(serializers.ModelSerializer):
    contenido_interactivo = ContenidoInteractivoDetailsSerializer(source='contenidointeractivo_set', many=True)
    estudiantes = serializers.SerializerMethodField()
    total_estudiantes = serializers.SerializerMethodField()
    fecha_creacion = serializers.SerializerMethodField()

    @staticmethod
    def get_estudiantes(obj):
        return EstudianteDetailsSerializer(Estudiante.objects.filter(grupo__curso=obj), many=True).data

    @staticmethod
    def get_total_estudiantes(obj):
        return Grupo.objects.filter(curso=obj).count()

    @staticmethod
    def get_fecha_creacion(obj):
        return obj.fecha_creacion.strftime("%Y-%m-%d")

    class Meta:
        model = Curso
        fields = ['id', 'nombre', 'descripcion', 'fecha_creacion', 'profesor', 'total_estudiantes', 'estudiantes',
                  'contenido_interactivo']
