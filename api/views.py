from rest_framework.generics import ListAPIView, RetrieveAPIView

from api.models import Curso, Aula
from api.rest_framework.pagination import DefaultPagination
from api.rest_framework.serializers import CursoSerializer, AulaSerializer


class DefaultListAPIView(ListAPIView):
    pagination_class = DefaultPagination


class ListarCursos(DefaultListAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


class ListarAulas(DefaultListAPIView):
    queryset = Aula.objects.all()
    serializer_class = AulaSerializer


class DetalhesCurso(RetrieveAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'curso_id'


class DetalhesAula(RetrieveAPIView):
    queryset = Aula.objects.all()
    serializer_class = AulaSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'aula_id'


class ListarTutoriais(DefaultListAPIView):
    queryset = Aula.objects.filter(curso__isnull=True)
    serializer_class = AulaSerializer


class ListarAulasDeCursos(DefaultListAPIView):
    serializer_class = AulaSerializer

    def get_queryset(self):
        curso_id = self.kwargs.get('curso_id')
        print(curso_id)
        return Aula.objects.filter(curso=curso_id)

