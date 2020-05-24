from decimal import Decimal

from rest_framework import serializers
from rest_framework.fields import IntegerField, CharField

from activities.models import PreguntaOpcionMultiple, \
    RespuestmultipleEstudiante, Opcionmultiple, Calificacion, Marca, \
    PreguntaFoV, Pausa, PreguntaAbierta, RespuestaAbiertaEstudiante, \
    RespuestaVoF, Actividad
from interactive_content.models import ContenidoInteractivo


class RespuestaSeleccionMultipleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestmultipleEstudiante
        fields = '__all__'


class QualificationMultipleChoiceResponseSerializer(RespuestaSeleccionMultipleSerializer):
    qualification = serializers.SerializerMethodField()

    def get_qualification(self, _):
        total_options = Opcionmultiple.objects.filter(preguntaSeleccionMultiple=self.instance.respuestmultiple.preguntaSeleccionMultiple).count()
        total_incorrect_options = Opcionmultiple.objects.filter(preguntaSeleccionMultiple=self.instance.respuestmultiple.preguntaSeleccionMultiple, esCorrecta=False).count()
        note_by_option = Decimal(1/total_options) if total_options > 0 else 0
        base_note = note_by_option * total_incorrect_options
        qualification, _ = Calificacion.objects.get_or_create(
            estudiante=self.instance.estudiante, actividad=self.instance.respuestmultiple.preguntaSeleccionMultiple, defaults={"calificacion": base_note}
        )
        qualification.calificacion = qualification.calificacion + note_by_option if self.instance.respuestmultiple.esCorrecta else qualification.calificacion - note_by_option
        qualification.save()
        return qualification.calificacion


class RespuestaAbiertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestaAbiertaEstudiante
        fields = '__all__'


class RespuestaFoVSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestaVoF
        fields = '__all__'


class QualificationFoVResponseSerializer(RespuestaFoVSerializer):
    qualification = serializers.SerializerMethodField()

    def get_qualification(self, _):
        note = 1 if self.instance.preguntaVoF.esVerdadero == self.instance.esVerdadero else 0
        Calificacion.objects.update_or_create(
            estudiante=self.instance.estudiante, actividad=self.instance.preguntaVoF, defaults={"calificacion": note}
        )
        return note

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
    qualification = serializers.SerializerMethodField()

    def get_qualification(self, obj):
        self
        qualification = Calificacion.objects.filter(actividad=obj).first()
        return qualification.calificacion if qualification else 0

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
    qualification = serializers.SerializerMethodField()

    def get_qualification(self, obj):
        qualification = Calificacion.objects.filter(actividad=obj).first()
        return qualification.calificacion if qualification else 0

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

    class Meta:
        model = Actividad
        fields = ["tipoActividad", "marca_id", "nombre", "punto", "contenido"]


class ActividadPreguntaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = ["id", "retroalimentacion"]


class MarcaSerializerRetroalimentacion(serializers.ModelSerializer):
    actividades = serializers.SerializerMethodField('get_act')

    def get_act(self, marca):
        qs = Actividad.objects.filter(marca=marca)
        serializer = ActividadPreguntaSerializer(instance=qs, many=True)
        return serializer.data
    class Meta:
        model = Marca
        fields = ["id", "actividades"]


class ContenidoInteractivoRetroalimentacionSerializer(serializers.ModelSerializer):
    marcas = MarcaSerializerRetroalimentacion(read_only=True, many=True)

    class Meta:
        model = ContenidoInteractivo
        fields = fields = ["id", "marcas"]
