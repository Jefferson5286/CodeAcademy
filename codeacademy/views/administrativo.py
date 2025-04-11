from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages

from api.models import Curso, Aula

def painel_administrativo(request):
    return render(request, 'administrativo/painel_administrativo.html')


def ver_cursos(request):
    if request.method == 'POST':
        curso_ids = request.POST.getlist('curso_ids')
        if curso_ids:
            Curso.objects.filter(id__in=curso_ids).delete()
            return redirect('ver_cursos')

    cursos = Curso.objects.all()
    paginator = Paginator(cursos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'administrativo/ver_cursos.html', {'page_obj': page_obj})



# Ver Aulas
def ver_aulas(request):
    if request.method == 'POST':
        aula_ids = request.POST.getlist('aula_ids')

        if aula_ids:
            Aula.objects.filter(id__in=aula_ids).delete()
            return redirect('ver_aulas')

    aulas = Aula.objects.all()

    paginator = Paginator(aulas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'administrativo/ver_aulas.html', {'page_obj': page_obj})


# Página de um Curso Específico
def curso_detail(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    aulas_list = Aula.objects.filter(curso=curso).order_by('order')

    paginator = Paginator(aulas_list, 10)  # 10 aulas por página
    page_number = request.GET.get('page')
    aulas = paginator.get_page(page_number)

    return render(request, 'administrativo/curso_detail.html', {'curso': curso, 'aulas': aulas})


# Página de uma Aula Específica
def aula_detail(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)
    return render(request, 'administrativo/aula_detail.html', {'aula': aula})


# Criar Curso
def criar_curso(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Curso.objects.create(title=title, description=description)
        return redirect('ver_cursos')
    return render(request, 'administrativo/criar_curso.html')


# Criar Aula
def criar_aula(request):
    cursos = Curso.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        content = request.POST.get('content')
        curso_id = request.POST.get('curso')
        order = request.POST.get('order')

        curso = Curso.objects.get(id=curso_id) if curso_id else None

        # Validação
        if curso:
            # Aula faz parte de um curso
            if not order:
                messages.error(request, 'O campo "ordem" é obrigatório quando a aula pertence a um curso.')
                return render(request, 'administrativo/criar_aula.html', {'cursos': cursos})

            try:
                last_aula = Aula.objects.filter(curso=curso).order_by('-order').first()
                expected_order = (last_aula.order + 1) if last_aula else 1

                if int(order) != expected_order:
                    messages.error(request, f'A ordem da nova aula deve ser {expected_order}.')
                    return render(request, 'administrativo/criar_aula.html', {'cursos': cursos})

            except ValueError:
                messages.error(request, 'A ordem deve ser um número inteiro válido.')
                return render(request, 'administrativo/criar_aula.html', {'cursos': cursos})

        # Se passou todas as validações
        Aula.objects.create(
            title=title,
            description=description,
            content=content,
            curso=curso,
            order=order or 0
        )
        return redirect('ver_aulas')

    return render(request, 'administrativo/criar_aula.html', {'cursos': cursos})


# Excluir Cursos Selecionados
def excluir_cursos(request):
    if request.method == 'POST':
        ids = request.POST.getlist('selected_ids')
        Curso.objects.filter(id__in=ids).delete()
    return redirect('ver_cursos')


# Excluir Aulas Selecionadas
def excluir_aulas(request):
    if request.method == 'POST':
        ids = request.POST.getlist('selected_ids')
        Aula.objects.filter(id__in=ids).delete()
    return redirect('ver_aulas')


# Editar Aula
def editar_aula(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)
    cursos = Curso.objects.all()

    if request.method == 'POST':
        aula.title = request.POST.get('title')
        aula.description = request.POST.get('description')
        aula.content = request.POST.get('content')
        curso_id = request.POST.get('curso')
        aula.curso = Curso.objects.get(id=curso_id) if curso_id else None
        aula.order = request.POST.get('order') or 0
        aula.save()

        return redirect('ver_aula', aula_id=aula.id)

    return render(request, 'administrativo/editar_aula.html', {'aula': aula, 'cursos': cursos})


# Excluir Aula Individual
def excluir_aula(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)
    if request.method == 'POST':
        aula.delete()
        return redirect('ver_aulas')

    return render(request, 'administrativo/excluir_aula_confirm.html', {'aula': aula})


def excluir_aulas_selecionadas(request):
    if request.method == 'POST':
        aula_ids = request.POST.getlist('aula_ids')
        curso_id = request.POST.get('curso_id')

        if aula_ids:
            Aula.objects.filter(id__in=aula_ids).delete()

        return redirect('ver_curso', curso_id=curso_id)