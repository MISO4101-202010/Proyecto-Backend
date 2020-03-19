from activities.models import PreguntaAbierta


class PreguntaAbierta(ListModelMixin, CreateModelMixin, GenericAPIView):
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
