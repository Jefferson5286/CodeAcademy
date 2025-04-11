from django.urls import path
from api import views


urlpatterns = [
    path('cursos/', views.ListarCursos.as_view(), name='listar_cursos'),
    path('cursos/<uuid:curso_id>/aulas/', views.ListarAulasDeCursos.as_view(), name='listar_cursos_aulas'),
    path('cursos/<uuid:curso_id>/', views.DetalhesCurso.as_view(), name='detalhes_curso'),

    path('aulas/tutoriais/', views.ListarTutoriais.as_view(), name='listar_tutoriais'),
    path('aulas/<uuid:aula_id>/', views.DetalhesAula.as_view(), name='detalhes_aula'),
]