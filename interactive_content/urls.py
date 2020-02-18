from django.conf.urls import url
from django.urls import path

from interactive_content import views
from interactive_content.views import GetCourseView

app_name = 'interactiveContent'

urlpatterns = [
    url(r'^courses/$', views.courses_view, name='resources'),
    url(r'^generate-content/', views.ContentCreator.as_view(), name='create_content'),
    url(r'^interactive_content/$', views.interactive_contents_view, name='interactive_content'),
    url(r'^content/$', views.contents_view, name='content'),
    path('cont_interactivo', views.ContInteractivoView.as_view(), name='cont_interactivo'),
    path('mycourses', views.get_student_courses_and_interactive_content, name='get_student_courses_and_interactive_content'),
    url(r'^courses/(?P<content_id>\d+)/$', views.courses_content_view, name='courses'),
    url(r'^interactivecontent/(?P<pk>[0-9]+)$', views.ContenidoInteractivoDetail.as_view(), name='interactive_content'),
    path('courses/details/', GetCourseView.as_view(), name="info courses")
]
