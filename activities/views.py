from django import db
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from activities.models import Calificacion, Marca, RespuestmultipleEstudiante, Opcionmultiple, PreguntaOpcionMultiple, \
    PreguntaFoV, RespuestaVoF, Pausa, PreguntaAbierta, Actividad, RespuestaAbiertaEstudiante
from activities.serializers import PreguntaOpcionMultipleSerializer, CalificacionSerializer, \
    RespuestaSeleccionMultipleSerializer, MarcaSerializer, PreguntaFoVSerializer, PausaSerializer, \
    PreguntaAbiertaSerializer, RespuestaAbiertaSerializer, RespuestaFoVSerializer, \
    MarcaConTipoActividadSerializer, ActividadPreguntaSerializer, ContenidoInteractivoRetroalimentacionSerializer
from interactive_content.models import ContenidoInteractivo, Grupo, Curso
from interactive_content.permissions import IsProfesor
from users.models import Profesor, Estudiante


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def reports(request, contentpk):
    # Get correct professor through token or session
    try:
        get_the_professor = Profesor.objects.get(id=request.user.id)
    except:
        return HttpResponseNotFound()

    big_json = {}
    big_json['username'] = get_the_professor.username
    big_json['first_name'] = get_the_professor.first_name
    big_json['last_name'] = get_the_professor.last_name
    big_json['email'] = get_the_professor.email
    big_json['direccion'] = get_the_professor.direccion
    big_json['telefono'] = get_the_professor.telefono
    big_json['facultad'] = get_the_professor.facultad
    big_json['marcas'] = []

    marcas = Marca.objects.filter(
        contenido__contenido__profesor=get_the_professor, contenido_id=contentpk)
    for marca in marcas:

        big_json['marcas'].append({'nombre': marca.nombre, 'preguntas': []})
        preguntas_multiples = PreguntaOpcionMultiple.objects.filter(
            marca=marca)
        preguntas_vof = PreguntaFoV.objects.filter(marca=marca)

        for pregunta in preguntas_multiples:
            if isinstance(pregunta, PreguntaOpcionMultiple):
                big_json['marcas'][-1]['preguntas'].append(
                    {'pregunta': pregunta.enunciado, 'tipo': 'multiple', 'total_respuestas': 0, 'opciones': []})
                opciones = Opcionmultiple.objects.filter(
                    preguntaSeleccionMultiple=pregunta)

                cont = 0
                for opcion in opciones:
                    votos = RespuestmultipleEstudiante.objects.filter(
                        respuestmultiple=opcion).count()
                    cont += votos
                    big_json['marcas'][-1]['preguntas'][-1]['opciones'].append(
                        {'respuesta': opcion.opcion, 'esCorrecta': opcion.esCorrecta, 'votos': votos})
                big_json['marcas'][-1]['preguntas'][-1]['total_respuestas'] = cont

        for pregunta in preguntas_vof:
            if isinstance(pregunta, PreguntaFoV):
                big_json['marcas'][-1]['preguntas'].append({'pregunta': pregunta.pregunta, 'esCorrecta': pregunta.esVerdadero,
                     'tipo': 'verdadero/falso', 'total_verdadero': 0, 'total_falso': 0, 'total_respuestas': 0})
                howManyTrue = RespuestaVoF.objects.filter(
                    preguntaVoF=pregunta, esVerdadero=True).count()  # "howTrue":value
                howManyFalse = RespuestaVoF.objects.filter(
                    preguntaVoF=pregunta, esVerdadero=False).count()  # "howFalse":value
                total_vf = howManyTrue + howManyFalse
                big_json['marcas'][-1]['preguntas'][-1]['total_verdadero'] = howManyTrue
                big_json['marcas'][-1]['preguntas'][-1]['total_falso'] = howManyFalse
                big_json['marcas'][-1]['preguntas'][-1]['total_respuestas'] = total_vf

    return JsonResponse(big_json)


class MarcaView(ListModelMixin, CreateModelMixin, GenericAPIView):
    # Add permissions to the view
    # permission_classes = [IsAuthenticated]

    # queryset usado para retornar los objetos requeridos
    def get_queryset(self):
        # Add filter to get all the activities of a desired Marca
        contenido = self.request.query_params.get('contenido', None)
        return Marca.objects.filter(contenido=contenido)

    # clase serializer para la transformacion de datos del request
    serializer_class = MarcaSerializer

    def perform_create(self, serializer):
        contenido = get_object_or_404(
            ContenidoInteractivo, id=self.request.data.get('contenido'))
        return serializer.save(contenido=contenido)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        marca_id = self.request.data.get('marca_id')
        marca = get_object_or_404(Marca, id =marca_id)
        marca.nombre = self.request.data.get('nombre')
        marca.punto = self.request.data.get('punto')
        marca.save()
        return Response(data=MarcaSerializer(marca).data)


def createOrGetMarca(question_data):
    marca_id = question_data.pop('marca_id', None)
    marca = None
    if not marca_id:
        interactive_content = ContenidoInteractivo.objects.get(
            id=question_data['marca'].pop('contenido_id'))
        marca = Marca.objects.create(
            contenido=interactive_content, **question_data.pop('marca'))
    else:
        marca = Marca.objects.get(pk=marca_id)
    return marca


class CreatePreguntaAbierta(RetrieveUpdateAPIView):
    queryset = PreguntaAbierta.objects.all()
    serializer_class = PreguntaAbiertaSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsProfesor]

    def put(self, request, *args, **kwargs):
        question_data = request.data

        try:
            marca_id = question_data.get('marca_id')
        except:
            marca_id = None

        try:
            abierta_id = question_data.get('abierta_id')
        except:
            abierta_id = None

        if question_data.get('numeroDeIntentos') is None:
            question_data['numeroDeIntentos'] = 1

        marca = createOrGetMarca(question_data)

        if marca_id is None:
            question = PreguntaAbierta.objects.create(marca=marca, **question_data)
        else:
            question = PreguntaAbierta.objects.get(id=abierta_id)
            question.nombre = question_data['nombre']
            question.enunciado = question_data['enunciado']
            question.save()
        return Response(data=PreguntaAbiertaSerializer(question).data, status=status.HTTP_201_CREATED)



def index_of(val, in_list):
    try:
        return in_list.index(val)
    except ValueError:
        return -1


class CreatePreguntaSeleccionMultiple(RetrieveUpdateAPIView):
    queryset = PreguntaOpcionMultiple.objects.all()
    serializer_class = PreguntaOpcionMultipleSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsProfesor]

    def put(self, request, *args, **kwargs):
        question_data = request.data
        try:
            marca_id = question_data.get('marca_id')
        except:
            marca_id = None

        try:
            seleccion_multiple_id = question_data.get('seleccion_multiple_id')
        except:
            seleccion_multiple_id = None

        marca = createOrGetMarca(question_data)

        if marca_id is None:
            options = question_data.pop('opciones')
            question = PreguntaOpcionMultiple.objects.create(
                marca=marca, **question_data)
            for option in options:
                Opcionmultiple.objects.create(
                    preguntaSeleccionMultiple=question, **option)
        else:
            question = PreguntaOpcionMultiple.objects.get(id=seleccion_multiple_id)
            question.enunciado = question_data['enunciado']
            question.esMultipleResp = question_data['esMultipleResp']
            question.nombre = question_data['nombre']
            question.tieneRetroalimentacion = question_data['tieneRetroalimentacion']
            question.numeroDeIntentos = question_data['numeroDeIntentos']
            question.save()
            options = question_data.get('opciones')
            listOption = [o.get('opcion_id') for o in options]
            #validar eliminados
            options_ = Opcionmultiple.objects.filter(preguntaSeleccionMultiple_id=seleccion_multiple_id);
            for option in options_:
                if index_of(option.id, listOption) == -1:
                 option.delete()
            for option in options:
                try:
                    option_id = option.get('opcion_id')
                except:
                    option_id = None
                if option_id is None:
                    Opcionmultiple.objects.create(
                        preguntaSeleccionMultiple=question, **option)
                else:
                    option_ = Opcionmultiple.objects.get(id=option_id);
                    option_.esCorrecta = option.get('esCorrecta')
                    option_.opcion = option.get('opcion')
                    option_.save()

        return Response(data=PreguntaOpcionMultipleSerializer(question).data, status=status.HTTP_201_CREATED)


class PreguntaFoVView(ListModelMixin, CreateModelMixin, GenericAPIView):
    serializer_class = PreguntaFoVSerializer

    def get(self, request, *args, **kwargs):
        questions = PreguntaFoV.objects.all()
        serializer = PreguntaFoVSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        question_data = request.data
        marca_id = question_data.get('marca', None)
        if not marca_id:
            interactive_content = ContenidoInteractivo.objects.get(
                id=question_data['marca'].pop('contenido_id'))
            marca = Marca.objects.create(
                contenido=interactive_content, **question_data.pop('marca'))
        else:
            marca = Marca.objects.get(pk=marca_id)
        question_data.pop('marca')
        question = PreguntaFoV.objects.create(marca=marca, **question_data)
        return Response(PreguntaFoVSerializer(question).data, status=status.HTTP_201_CREATED)


class PreguntaFoVGetOne(ListModelMixin, CreateModelMixin, GenericAPIView):
    serializer_class = PreguntaFoVSerializer

    def get(self, request, *args, **kwargs):
        marca = self.kwargs.get('marca', None)
        questions = PreguntaFoV.objects.filter(marca=marca)
        if questions.count() > 1:
            return Response('Múltiples resultados para la marca ' + str(marca), status=status.HTTP_404_NOT_FOUND)
        serializer = PreguntaFoVSerializer(questions.get())
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetPausesView(generics.RetrieveUpdateDestroyAPIView, ListModelMixin):
    serializer_class = PausaSerializer
    lookup_url_kwarg = "marca"

    def get_queryset(self):
        marca = self.kwargs.get(self.lookup_url_kwarg)
        return Pausa.objects.filter(marca=marca)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)


class GetPreguntaAbierta(APIView):
    def get(self, request, *args, **kwargs):
        marca = self.kwargs.get('marca', None)
        questions = PreguntaAbierta.objects.filter(marca=marca)
        serializer = PreguntaAbiertaSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetailPreguntaAbierta(generics.RetrieveUpdateDestroyAPIView, ListModelMixin):
    serializer_class = PreguntaAbiertaSerializer
    lookup_url_kwarg = "marca"

    def get_queryset(self):
        marca = self.kwargs.get(self.lookup_url_kwarg)
        return PreguntaAbierta.objects.filter(marca=marca)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)


class DetailPreguntaSeleccionMultiple(generics.RetrieveUpdateDestroyAPIView, ListModelMixin):
    serializer_class = PreguntaOpcionMultipleSerializer
    lookup_url_kwarg = "marca"

    def get_queryset(self):
        marca = self.kwargs.get(self.lookup_url_kwarg)
        return PreguntaOpcionMultiple.objects.filter(marca=marca)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)


class PreguntaView(ListModelMixin, CreateModelMixin, GenericAPIView):
    # Add permissions to the view
    # permission_classes = [IsAuthenticated]

    # Add filter fields for the API
    filterset_fields = ("actividad",)
    # clase serializer para la transformacion de datos del request
    serializer_class = PreguntaOpcionMultipleSerializer

    # def get_queryset(self):
    # actividad = self.request.query_params.get('actividad')
    # return PreguntaOpcionMultiple.objects.filter(actividad=actividad)

    def perform_create(self, serializer):
        # actividad = get_object_or_404(
        #    Actividad, id=self.request.data.get('actividad'))
        return serializer.save()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RespuestaSeleccionMultipleView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = RespuestmultipleEstudiante.objects.all()
    # clase serializer para la transformacion de datos del request
    serializer_class = RespuestaSeleccionMultipleSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # Validacion de respuesta en blanco (null)
        if self.request.data['respuestmultiple']:
            opcion = Opcionmultiple.objects.filter(
                id=self.request.data['respuestmultiple'])
            pregunta = opcion[0].preguntaSeleccionMultiple
            # valida si el intento de la respuesta es menor o igual al max de intentos permitidos
            if int(self.request.data['intento']) <= pregunta.numeroDeIntentos:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                msj = {'max_attemps': 'Número de intentos maximos excedido'}
                return Response(msj, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CalificarAPI(ListCreateAPIView):
    # Add filter fields for the API
    filterset_fields = ("estudiante", "actividad")
    # serializer usado para la transformacion de datos
    serializer_class = CalificacionSerializer

    # queryset para retornar las calificaciones de un estudiante
    def get_queryset(self):
        student = self.request.query_params.get('estudiante', None)
        activity = self.request.query_params.get('actividad', None)
        if (student):
            return Calificacion.objects.filter(estudiante=student)
        elif (activity):
            return Calificacion.objects.filter(actividad=activity)
        else:
            return Calificacion.objects.filter(actividad=None)


class MarcaApi(ListModelMixin, GenericAPIView):
    pagination_class = None

    def get_serializer_class(self):
        contenido = self.request.query_params.get('contenido', None)
        if contenido is not None:
            return MarcaConTipoActividadSerializer
        return MarcaSerializer

    def get(self, request, *args, **kwargs):
        try:
            content = self.request.query_params.get('contenido', None)
            marca = self.request.query_params.get('marca', None)
            if content is not None:
                data = retrieve_mark_information(content)
                return JsonResponse(data, status=status.HTTP_200_OK, safe=False)
            elif marca is not None:
                return JsonResponse(MarcaSerializer(Marca.objects.filter(pk=marca), many=True).data,
                                    status=status.HTTP_200_OK, safe=False)
            else:
                return JsonResponse(MarcaSerializer(Marca.objects.all(), many=True).data, status=status.HTTP_200_OK,
                                    safe=False)
        except:
            return JsonResponse({'msj': 'Error procesando el request'}, status=status.HTTP_200_OK)



def intentos_max(request):
    if request.method == 'GET':
        pregunta = request.GET.get('id_pregunta')
        estudiante = request.GET.get('id_estudiante')
        tipo_preg = Actividad.objects.get(id=pregunta).tipoActividad
        max_int = retrieve_max_intentos(tipo_preg, estudiante, pregunta)

        return JsonResponse({'ultimo_intento': max_int}, status=status.HTTP_200_OK)


def retrieve_max_intentos(tipo, user, pregunta):
    if tipo == 1:
        opciones = Opcionmultiple.objects.filter(
            preguntaSeleccionMultiple=pregunta)

        respuestas = RespuestmultipleEstudiante.objects.filter(
            estudiante=user)
        resps = get_intento_estudiante(respuestas, opciones)
        return validate_resps(resps)

    if tipo == 2:
        respuestas = RespuestaVoF.objects.filter(
            estudiante=user).filter(preguntaVoF=pregunta)

        return consolida_resps(respuestas)

    if tipo == 3:
        respuestas = RespuestaAbiertaEstudiante.objects.filter(
            estudiante=user).filter(preguntaAbierta=pregunta)

        return consolida_resps(respuestas)


def consolida_resps(respuestas):
    resps = []
    for resp in respuestas:
        resps.append(resp.intento)

    return validate_resps(resps)


def get_intento_estudiante(respuestas, opciones):
    resps = []

    for respuesta in respuestas:
        for opcion in opciones:
            if respuesta.respuestmultiple == opcion:
                if respuesta.intento:
                    resps.append(respuesta.intento)
    return resps


def validate_resps(resps):
    if len(resps) > 0:
        max_int = max(resps)
    else:
        max_int = 0

    return max_int


class PausaDetail(RetrieveUpdateAPIView):
    queryset = Pausa.objects.all()
    serializer_class = PausaSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsProfesor]

    def put(self, request, *args, **kwargs):
        question_data = request.data
        marca_id = None
        pausa_id = None
        try:
            marca_id = question_data.get('marca_id')
        except:
            marca_id = None

        try:
            pausa_id = question_data.pop('pausa_id', None)
        except:
            pausa_id = None
        marca = createOrGetMarca(question_data)
        if marca_id is None:
            question = Pausa.objects.create(marca=marca, **question_data)
        else:
            marca.nombre = question_data['nombre']
            marca.save()
            question = Pausa.objects.get(id=pausa_id)
            question.tiempo = question_data['tiempo']
            question.enunciado = question_data['enunciado']
            question.save()

        return Response(data=PausaSerializer(question).data, status=status.HTTP_201_CREATED)


def tipo_actividad(request):
    if request.method == 'GET':
        marca = request.GET.get('id_marca')
        activity = Actividad.objects.filter(marca=marca)

        return JsonResponse({'tipo_actividad': activity[0].tipoActividad})


class RespuestaAbiertaView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = RespuestaAbiertaEstudiante.objects.all()
    # clase serializer para la transformacion de datos del request
    serializer_class = RespuestaAbiertaSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # Validacion de respuesta en blanco (null)
        if self.request.data['preguntaAbierta']:
            pregunta1 = PreguntaAbierta.objects.filter(
                id=self.request.data['preguntaAbierta']
            )
            print('xxxx', pregunta1)
            pregunta = pregunta1[0]

            # pregunta = pregunta1[0].preguntaSeleccionMultiple
            # valida si el intento de la respuesta es menor o igual al max de intentos permitidos
            if int(self.request.data['intento']) <= pregunta.numeroDeIntentos:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                msj = {'max_attemps': 'Número de intentos maximos excedido'}
                return Response(msj, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            print('no pasa')
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RespuestaFoVMultipleView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = RespuestaVoF.objects.all()
    # clase serializer para la transformacion de datos del request
    serializer_class = RespuestaFoVSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # Validacion de respuesta en blanco (null)
        if self.request.data['preguntaVoF']:
            pregunta1 = PreguntaFoV.objects.filter(
                id=self.request.data['preguntaVoF']
            )
            pregunta = pregunta1[0]

            # pregunta = pregunta1[0].preguntaSeleccionMultiple
            # valida si el intento de la respuesta es menor o igual al max de intentos permitidos
            if int(self.request.data['intento']) <= pregunta.numeroDeIntentos:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                msj = {'max_attemps': 'Número de intentos maximos excedido'}
                return Response(msj, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RespuestaFoVView(ListModelMixin, CreateModelMixin, GenericAPIView):
    serializer_class = RespuestaFoVSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        '''Validar si la información necesaria viene'''
        # Validar extraer los datos del request
        preguntaVoF_id = self.request.data['preguntaVoF']
        estudiante_id = self.request.data['estudiante']
        respuesta_actual = self.request.data['esVerdadero']
        if preguntaVoF_id is not None and estudiante_id is not None and respuesta_actual is not None:
            try:
                respuesta_previa = RespuestaVoF.objects.filter(preguntaVoF=preguntaVoF_id,
                                                               estudiante_id=estudiante_id).latest('id')
            except:
                respuesta_previa = None

            if respuesta_previa is not None:
                if respuesta_previa.preguntaVoF.numeroDeIntentos > respuesta_previa.intento:
                    nueva_respuesta = RespuestaVoF()
                    nueva_respuesta.preguntaVoF = respuesta_previa.preguntaVoF
                    nueva_respuesta.intento = respuesta_previa.intento + 1
                    nueva_respuesta.grupo = respuesta_previa.grupo
                    nueva_respuesta.estudiante = respuesta_previa.estudiante
                    nueva_respuesta.esVerdadero = respuesta_actual
                    nueva_respuesta.save()
                    return Response(self.serializer_class(nueva_respuesta).data, status=status.HTTP_200_OK)
                else:
                    return Response(data={"Máximo número de intentos alcanzado"}, status=status.HTTP_400_BAD_REQUEST)

            else:
                # obtener pregunta
                pregunta = PreguntaFoV.objects.filter(pk=preguntaVoF_id).get()
                # obtenerEstudiante
                estudianteObj = Estudiante.objects.filter(pk=estudiante_id).get()
                # Obtener grupo
                # TODO Refactor para buscar el grupo según el estudiante y el grupo
                grupo = Grupo.objects.all().first()
                # Crear respuesta
                respuestaFoV = RespuestaVoF()
                respuestaFoV.estudiante = estudianteObj
                respuestaFoV.esVerdadero = respuesta_actual
                respuestaFoV.intento = 1
                respuestaFoV.grupo = grupo
                respuestaFoV.preguntaVoF = pregunta
                respuestaFoV.save()
                return Response(self.serializer_class(respuestaFoV).data, status=status.HTTP_200_OK)
        else:
            return Response(data={"Campos obligatorios no incluidos"}, status=status.HTTP_400_BAD_REQUEST)


def retrieve_mark_information(contenido):
    cursor = db.connection.cursor()
    ## TODO Hay un problema en este query y no se puede calcular el numero de intentos de la respuesta con opción multiple, porque el objeto de respuesta de opcion multiple no tiene asociada la pregunta a la cual le corresponde
    with open('activities/getInformacionMarca.sql', 'r') as file:
        query = file.read().replace('\n', ' ').replace('\t', ' ')
        cursor.execute(query, (contenido, contenido))
        return dictfetchall(cursor)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict."
    rows = cursor.fetchall()
    result = []
    keys = ('id','marca_id','tipoActividad','punto','nombre','contenido_id','numIntentos')
    for row in rows:
        result.append(dict(zip(keys, row)))
    return result


class PreguntaVoFModificacionViewSet(GenericViewSet, UpdateModelMixin):
    queryset = PreguntaFoV.objects.all()
    serializer_class = PreguntaFoVSerializer
    http_method_names = ['patch']

class GetRetroalimentacion(ListModelMixin, GenericAPIView):
    serializer_class = ContenidoInteractivoRetroalimentacionSerializer
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs.get(self.lookup_url_kwarg)
        # interactive_content = ContenidoInteractivo.objects.get(id=id)

        return ContenidoInteractivo.objects.filter(id=id)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

class GetRetroalimentacionPregunta(ListModelMixin, GenericAPIView):
    serializer_class = ActividadPreguntaSerializer
    lookup_url_kwarg = "id"

    def get_queryset(self):
        marca = self.kwargs.get(self.lookup_url_kwarg)
        return Actividad.objects.filter(id=marca,tieneRetroalimentacion=True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)
