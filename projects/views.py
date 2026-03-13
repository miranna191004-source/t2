from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Project, ProjectMember, Favorite
from .forms import ProjectForm


def project_list(request):
    projects = Project.objects.select_related('owner').all()
    paginator = Paginator(projects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'projects/project_list.html', {'page_obj': page_obj})


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    members = project.members.all()
    is_owner = request.user.id == project.owner.id
    is_member = request.user in [m.user for m in members] if request.user.is_authenticated else False
    is_favorite = Favorite.objects.filter(
        user=request.user,
        project=project
    ).exists() if request.user.is_authenticated else False

    return render(request, 'projects/project-details.html', {
        'project': project,
        'members': members,
        'is_owner': is_owner,
        'is_member': is_member,
        'is_favorite': is_favorite
    })


@login_required(login_url='login')
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            messages.success(request, 'Проект создан успешно!')
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()

    return render(request, 'projects/create-project.html', {
        'form': form,
        'title': 'Создать проект'
    })


@login_required(login_url='login')
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user.id != project.owner.id:
        messages.error(request, 'У вас нет прав редактировать этот проект.')
        return redirect('project_detail', project_id=project.id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Проект обновлен успешно!')
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projects/create-project.html', {
        'form': form,
        'project': project,
        'title': 'Редактировать проект'
    })


@login_required(login_url='login')
def join_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if not ProjectMember.objects.filter(project=project, user=request.user).exists():
        ProjectMember.objects.create(project=project, user=request.user)
        messages.success(request, f'Вы присоединились к проекту "{project.title}"')
    else:
        messages.info(request, 'Вы уже являетесь участником этого проекта.')

    return redirect('project_detail', project_id=project.id)


@login_required(login_url='login')
def complete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user.id != project.owner.id:
        messages.error(request, 'У вас нет прав завершить этот проект.')
        return redirect('project_detail', project_id=project.id)

    project.status = 'completed'
    project.save()
    messages.success(request, 'Проект завершен!')
    return redirect('project_detail', project_id=project.id)


@login_required(login_url='login')
@require_http_methods(["POST"])
def add_favorite(request, project_id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        project = get_object_or_404(Project, id=project_id)
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            project=project
        )

        if created:
            return JsonResponse({'success': True, 'favorited': True})
        else:
            return JsonResponse({'success': True, 'favorited': False})

    return JsonResponse({'error': 'Недопустимый запрос'}, status=400)


@login_required(login_url='login')
@require_http_methods(["POST"])
def remove_favorite(request, project_id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        project = get_object_or_404(Project, id=project_id)
        Favorite.objects.filter(user=request.user, project=project).delete()
        return JsonResponse({'success': True, 'favorited': False})

    return JsonResponse({'error': 'Недопустимый запрос'}, status=400)