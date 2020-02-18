from django.db.models import Subquery
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from users.models import Profesor
from interactive_content.permissions import IsProfesor
from interactive_content.models import Contenido, Curso, ContenidoInteractivo, Grupo
from interactive_content.serializers import CursoSerializer, ContenidoInteractivoSerializer, ContenidoSerializer, \
    CursoDetailsSerializer, ContenidoInteractivoFieldsSerializer


def get_interactive_contents(user_id):
    # Verificar que el docente tenga contenido creado
    try:
        # Recuperar el contenido que creó el profesor
        contents_list = ContenidoInteractivo.objects.filter(contenido__profesor_id=user_id).select_related('contenido')
    except (KeyError, ContenidoInteractivo.DoesNotExist):
        # devolver vacio si no existe contenido creado por el usuario
        return JsonResponse({})
    else:
        # Devolver los resultados de la consulta en formato JSON
        serializer_class = ContenidoInteractivoSerializer(contents_list, many=True)
        response = Response(serializer_class.data, status=status.HTTP_200_OK)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        return response


def get_contents(user_id):
    # Verificar que el docente tenga contenido creado
    try:
        # Recuperar el contenido que creó el profesor
        contents_list = Contenido.objects.filter(profesor_id=user_id)
    except (KeyError, Contenido.DoesNotExist):
        # devolver vacio si no existe contenido creado por el usuario
        return JsonResponse({})
    else:
        # Devolver los resultados de la consulta en formato JSON
        serializer_class = ContenidoSerializer(contents_list, many=True)
        response = Response(serializer_class.data, status=status.HTTP_200_OK)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        return response


def set_contents(resources, user_id):
    # Verificar que el docente sea el propietario del curso
    contenido_id = resources['contenido']
    cursos_ids = resources['cursos']
    ci = get_object_or_404(ContenidoInteractivo.objects.filter(contenido__profesor_id=user_id, pk=contenido_id))
    objetos = Curso.objects.filter(profesor_id=user_id, pk__in=cursos_ids)
    objetos = list(objetos)
    ci.curso.add(*objetos)
    return JsonResponse({'status': 'success'})

# Retorna la lista de cursos con su contenido interactivo para cada estudiante
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_student_courses_and_interactive_content(request):
    user = request.user
    print(type(user))
    print(isinstance(user, Profesor))
    if request.method == 'GET':
        data = []
        grupos = Grupo.objects.filter(estudiante=user)

        for grupo in grupos:
            data.append({"grupo":grupo.id,"curso":grupo.curso.id,"nombre":grupo.curso.nombre,"contenido_interactivo":[]})
            for element in ContenidoInteractivo.objects.filter(curso=grupo.curso):
                data[-1]['contenido_interactivo'].append(ContenidoInteractivoFieldsSerializer(element).data)

        return JsonResponse(data, safe=False)

# Verificar que solo sea un usuario profesor el que acceda a este endpoint
# Remove this authentication_classes. Only for testing
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def interactive_contents_view(request):
    # Tomando información del usuario
    user_id = request.user.id
    if request.method == 'GET':
        return get_interactive_contents(user_id)
    elif request.method == 'POST':
        resources = json.loads(request.body)
        return set_contents(resources, user_id)


# Verificar que solo sea un usuario profesor el que acceda a este endpoint
# Remove this authentication_classes. Only for testing
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def courses_content_view(request, content_id):
    # Tomando información del usuario
    user_id = request.user.id
    # Verificar que el docente tenga contenido creado
    try:
        # Recuperar el contenido que creó el profesor
        contents = ContenidoInteractivo.curso.through.objects.filter(contenidointeractivo_id=content_id)
        user = request.user
        user_with_roll = user.get_real_instance()
        if user_with_roll.__class__.__name__ == 'Profesor':
            if not contents:
                contents_list = Curso.objects.filter(profesor_id=user_id)
            else:
                contents_list = Curso.objects.filter(profesor_id=user_id).exclude(
                    pk__in=Subquery(contents.values('curso_id')))
        else:
            cursos_ids = Grupo.objects.filter(estudiante=user_with_roll).values_list('curso_id', flat=True)
            contents_list = Curso.objects.filter(pk__in=list(cursos_ids))

    except (KeyError, Curso.DoesNotExist):
        # devolver vacio si no existe contenido creado por el usuario
        return JsonResponse({})
    else:
        # Devolver los resultados de la consulta en formato JSON
        serializer_class = CursoSerializer(contents_list, many=True)
        response = Response(serializer_class.data, status=status.HTTP_200_OK)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        return response


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def courses_view(request):
    # Tomando información del usuario logueado
    user_id = request.user.id
    try:
        # Recuperar los cursos que creó el profesor
        user = request.user
        user_with_roll = user.get_real_instance()
        if user_with_roll.__class__.__name__ == 'Profesor':
            contents_list = Curso.objects.filter(profesor_id=user_id).filter()
        else:
            cursos_ids = Grupo.objects.filter(estudiante=user_with_roll).values_list('curso_id', flat=True)
            contents_list = Curso.objects.filter(pk__in=list(cursos_ids))
    except (KeyError, Curso.DoesNotExist):
        # devolver vacio si no existe contenido creado por el usuario
        return JsonResponse({})
    else:
        # Devolver los resultados de la consulta en formato JSON
        serializer_class = CursoSerializer(contents_list, many=True)
        response = Response(serializer_class.data, status=status.HTTP_200_OK)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        return response


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def contents_view(request):
    # Tomando información del usuario
    user_id = request.user.id
    if request.method == 'GET':
        return get_contents(user_id)


class ContentCreator(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        new_content_data = request.data
        courses = new_content_data.pop('cursos_seleccionados', None)
        user_with_roll = request.user.get_real_instance()
        contenido = Contenido.objects.create(profesor=user_with_roll, **new_content_data)
        if courses:
            interactive_content = ContenidoInteractivo.objects.create(contenido=contenido,
                                                                      tiene_retroalimentacion=False)
            for selected_course in courses:
                course_obj = Curso.objects.get(pk=selected_course['id'], profesor=request.user)
                interactive_content.curso.add(course_obj)
        return Response(status=status.HTTP_201_CREATED)


class ContInteractivoView(ListModelMixin, CreateModelMixin, GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # queryset usado para retornar los objetos requeridos
    queryset = ContenidoInteractivo.objects.all()
    # clase serializer para la transformacion de datos del request
    serializer_class = ContenidoInteractivoSerializer

    def perform_create(self, serializer):
        contenido = get_object_or_404(
            Contenido, id=self.request.data.get('contenido'))
        return serializer.save(contenido=contenido)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        user = request.user.get_real_instance()
        if user.__class__.__name__ == 'Profesor':
            new_content_data = request.data
            contenido_id = int(new_content_data['contenido'])
            user_id = user.id

            contenido = get_object_or_404(Contenido.objects.filter(profesor_id=user_id, pk=contenido_id))
            new_content_data['contenido'] = contenido

            ci = ContenidoInteractivo.objects.create(**new_content_data)

            serializer_class = ContenidoInteractivoSerializer(ci, many=False)
            response = Response(serializer_class.data, status=status.HTTP_200_OK)
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            return response
        else:
            return JsonResponse({'message': 'Unauthorized'}, status=401)


class ContenidoInteractivoDetail(RetrieveUpdateDestroyAPIView):
    queryset = ContenidoInteractivo.objects.all()
    serializer_class = ContenidoInteractivoSerializer
    authentication_classes = (TokenAuthentication,)


class GetCourseView(APIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsProfesor]

    @staticmethod
    def get(request):
        cursos = Curso.objects.filter(profesor=request.user)
        serializer = CursoDetailsSerializer(cursos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
