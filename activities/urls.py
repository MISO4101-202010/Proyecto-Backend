from django.urls import path, include
from rest_framework import routers

from activities.views import CalificarAPI, MarcaApi, intentos_max, GetPausesView, GetPreguntaAbierta, \
    MarcaView, reports, RespuestaSeleccionMultipleView, CreatePreguntaSeleccionMultiple, PausaDetail, \
    CreatePreguntaAbierta, DetailPreguntaSeleccionMultiple, \
    tipo_actividad, PreguntaFoVGetOne, PreguntaFoVView, \
    RespuestaFoVView, RespuestaAbiertaView, DetailPreguntaAbierta, PreguntaVoFModificacionViewSet, GetRetroalimentacion, \
    GetRetroalimentacionPregunta, GetReporteCalificaciones

app_name = 'activities'
# add url path to the API

router = routers.DefaultRouter()
router.register('pregunta_f_v/update', PreguntaVoFModificacionViewSet)

urlpatterns = [
    path('marca', MarcaView.as_view(), name='marca'),
    path('reports/<int:contentpk>', reports, name='reports'),
    path('respuestaOpcionMultiple/', RespuestaSeleccionMultipleView.as_view()),
    path('respuestaAbierta/', RespuestaAbiertaView.as_view()),
    path('respuestafov/', RespuestaFoVView.as_view()),
    path('preguntaOpcionMultiple/<int:marca>/', DetailPreguntaSeleccionMultiple.as_view()),
    path('preguntaAbierta/<int:marca>/', DetailPreguntaAbierta.as_view()),
    path('calificacion', CalificarAPI.as_view(), name='calificacion'),
    path('generate-question-multiple-choice', CreatePreguntaSeleccionMultiple.as_view(),
         name='pregunta seleccion multiple '),
    path('generate-open-question', CreatePreguntaAbierta.as_view(), name='pregunta abierta '),
    path('marcas', MarcaApi.as_view(), name='marcas'),
    path('ultimo_intento', intentos_max),
    path('pregunta_f_v/<int:marca>', PreguntaFoVGetOne.as_view(), name='preguntasFoV'),
    path('pregunta_f_v', PreguntaFoVView.as_view(), name='preguntasFoV'),
    path('pausas/<int:marca>/', GetPausesView.as_view(), name="get pauses"),
    path('pregunta_abierta', GetPreguntaAbierta.as_view(), name="pregunta abierta"),
    path('pregunta_abierta/<int:marca>/', GetPreguntaAbierta.as_view(), name="pregunta abierta"),
    path('create-pausa/', PausaDetail.as_view(), name="create pauses"),
    path('tipo_actividad', tipo_actividad),
    path('retroalimentacion/<int:id>/', GetRetroalimentacion.as_view()),
    path('retroalimentacion/pregunta/<int:id>/', GetRetroalimentacionPregunta.as_view()),
    path('calificaciones_reporte', GetReporteCalificaciones.as_view()),
    path('', include(router.urls)),
]
