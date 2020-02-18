from django.urls import path
from activities.views import CalificarAPI, MarcaApi, intentos_max, PreguntaFoVView, GetPausesView, GetPreguntaAbierta, \
    MarcaView, reports, RespuestaSeleccionMultipleView, CreatePreguntaSeleccionMultiple, PausaDetail, \
    CreatePreguntaAbierta, DetailPreguntaSeleccionMultiple, \
    tipo_actividad, RespuestaAbiertaMultipleView, RespuestaFoVMultipleView

app_name = 'activities'
# add url path to the API

urlpatterns = [
    path('marca', MarcaView.as_view(), name='marca'),
    path('reports/<int:contentpk>', reports, name='reports'),
    path('respuestaOpcionMultiple/', RespuestaSeleccionMultipleView.as_view()),
    path('respuestaAbierta/', RespuestaAbiertaMultipleView.as_view()),
    path('respuestafov/', RespuestaFoVMultipleView.as_view()),
    path('preguntaOpcionMultiple/<int:marca>/',
         DetailPreguntaSeleccionMultiple.as_view()),
    path('calificacion', CalificarAPI.as_view(), name='calificacion'),
    path('generate-question-multiple-choice', CreatePreguntaSeleccionMultiple.as_view(),
         name='pregunta seleccion multiple '),
    path('generate-open-question', CreatePreguntaAbierta.as_view(), name='pregunta abierta '),
    path('marca', MarcaApi.as_view(), name='marca'),
    path('ultimo_intento', intentos_max),
    path('pregunta_f_v/<int:marca>/',
         PreguntaFoVView.as_view(), name='preguntasFoV'),
    path('pregunta_f_v/create', PreguntaFoVView.as_view(), name='preguntasFoV'),
    path('pausas/<int:marca>/', GetPausesView.as_view(), name="get pauses"),
    path('pregunta_abierta', GetPreguntaAbierta.as_view(), name="pregunta abierta"),
    path('pregunta_abierta/<int:marca>/', GetPreguntaAbierta.as_view(), name="pregunta abierta"),
    path('create-pausa/', PausaDetail.as_view(), name="create pauses"),
    path('tipo_actividad', tipo_actividad),
]
