from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework import parsers, renderers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from users.models import Profesor
from users.serializers import ProfesorSerializer, EstudianteSerializer
from django.contrib.auth import user_logged_in


# Create your views here.


class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_with_roll = user.get_real_instance()
        if user_with_roll.__class__.__name__  == 'Profesor':
            user_serialized = ProfesorSerializer(user_with_roll).data
        else:
            user_serialized = EstudianteSerializer(user_with_roll).data
        token, created = Token.objects.get_or_create(user=user)
        user_logged_in.send(sender=user.__class__, request=request, user=user)
        return Response(data={
            'user': user_serialized,
            'token': token.key
        }, status=HTTP_200_OK)
