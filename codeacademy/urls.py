from django.urls import path
from codeacademy import views

urlpatterns = [
    path('administrativo/', views.painel_administrativo, name='painel_administrativo'),

    # Cursos
    path('administrativo/cursos/', views.ver_cursos, name='ver_cursos'),
    path('administrativo/cursos/criar/', views.criar_curso, name='criar_curso'),
    path('administrativo/cursos/<uuid:curso_id>/', views.curso_detail, name='ver_curso'),
    path('administrativo/cursos/excluir/', views.excluir_cursos, name='excluir_cursos'),

    # Aulas
    path('administrativo/aulas/', views.ver_aulas, name='ver_aulas'),
    path('administrativo/aulas/criar/', views.criar_aula, name='criar_aula'),
    path('administrativo/aulas/<uuid:aula_id>/', views.aula_detail, name='ver_aula'),
    path('administrativo/aulas/<uuid:aula_id>/editar/', views.editar_aula, name='editar_aula'),
    path('administrativo/aulas/excluir/', views.excluir_aulas, name='excluir_aulas'),
    path('administrativo/aulas/<uuid:aula_id>/excluir/', views.excluir_aula, name='excluir_aula'),
]
