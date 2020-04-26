from rest_framework import serializers
from rest_framework.fields import SerializerMethodField, IntegerField, CharField

from activities.models import PreguntaOpcionMultiple, RespuestmultipleEstudiante, Opcionmultiple, Calificacion, Marca, \
    PreguntaFoV, Pausa, PreguntaAbierta, RespuestaAbiertaEstudiante, RespuestaVoF, Actividad


class RespuestaSeleccionMultipleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestmultipleEstudiante
        fields = '__all__'

class RespuestaAbiertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestaAbiertaEstudiante
        fields = '__all__'

class RespuestaFoVSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestaVoF
        fields = '__all__'

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = ('id', 'estudiante', 'actividad', 'calificacion')


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'


class OpcionmultipleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcionmultiple
        fields = '__all__'


class PreguntaOpcionMultipleSerializer(serializers.ModelSerializer):
    opciones = OpcionmultipleSerializer(read_only=True, many=True)

    class Meta:
        model = PreguntaOpcionMultiple
        fields = '__all__'


class PreguntaAbiertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreguntaAbierta
        fields = '__all__'


class OpcionMultipleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcionmultiple
        fields = '__all__'


class PreguntaFoVSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreguntaFoV
        fields = '__all__'


class PreguntaFoVModificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreguntaFoV
        fields = ('pregunta', 'nombre', 'retroalimentacion', 'numeroDeIntentos', 'esVerdadero', 'tieneRetroalimentacion')


class PausaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pausa
        fields = '__all__'


class PreguntaAbiertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreguntaAbierta
        fields = '__all__'


class MarcaConTipoActividadSerializer(serializers.ModelSerializer):
    marca_id = IntegerField(source="marca.id")
    nombre = CharField(source="marca.nombre")
    punto = IntegerField(source="marca.punto")
    contenido = IntegerField(source="marca.contenido_id")
    #numIntentosFaltantes =

    class Meta:
        model = Actividad
        fields = ["tipoActividad", "marca_id", "nombre", "punto", "contenido"]
