from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import CustomUser, Skill, UserSkill
from .forms import (
    CustomUserCreationForm, CustomUserChangeForm, PasswordChangeForm,
    UserSkillForm
)
from projects.models import Project


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Регистрация успешна! Пожалуйста, войдите.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})

def home(request):
    projects = Project.objects.select_related('owner').all()
    paginator = Paginator(projects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'base.html', {'page_obj': page_obj})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.first_name}!')
                return redirect('home')
            else:
                messages.error(request, 'Неверный пароль.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Пользователь не найден.')

    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы.')
    return redirect('home')


def user_list(request):
    skill_filter = request.GET.get('skill', '')
    users = CustomUser.objects.all().prefetch_related('skills')

    if skill_filter:
        users = users.filter(skills__skill__name=skill_filter).distinct()

    paginator = Paginator(users, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    skills = Skill.objects.all()

    return render(request, 'users/participants.html', {
        'page_obj': page_obj,
        'skills': skills,
        'selected_skill': skill_filter
    })


def user_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    projects = Project.objects.filter(owner=user)
    skills = user.skills.all()
    is_owner = request.user.id == user_id

    return render(request, 'users/user-details.html', {
        'profile_user': user,
        'projects': projects,
        'skills': skills,
        'is_owner': is_owner
    })


@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен успешно!')
            return redirect('profile', user_id=request.user.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.check_password(form.cleaned_data['current_password']):
                if form.cleaned_data['new_password1'] == form.cleaned_data['new_password2']:
                    user.set_password(form.cleaned_data['new_password1'])
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Пароль изменен успешно!')
                    return redirect('profile', user_id=user.id)
                else:
                    messages.error(request, 'Новые пароли не совпадают.')
            else:
                messages.error(request, 'Текущий пароль неверен.')
    else:
        form = PasswordChangeForm()

    return render(request, 'users/change_password.html', {'form': form})


@login_required(login_url='login')
@require_http_methods(["POST"])
def add_skill(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        skill_name = request.POST.get('skill_name', '').strip()

        if not skill_name:
            return JsonResponse({'error': 'Название навыка не может быть пустым'}, status=400)

        skill, created = Skill.objects.get_or_create(name=skill_name)
        user_skill, created = UserSkill.objects.get_or_create(
            user=request.user,
            skill=skill
        )

        if created:
            return JsonResponse({
                'success': True,
                'message': f'Навык "{skill_name}" добавлен',
                'skill_id': skill.id,
                'skill_name': skill.name
            })
        else:
            return JsonResponse({
                'error': f'Навык "{skill_name}" уже добавлен'
            }, status=400)

    return JsonResponse({'error': 'Недопустимый запрос'}, status=400)


@login_required(login_url='login')
@require_http_methods(["POST"])
def remove_skill(request, skill_id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user_skill = get_object_or_404(UserSkill, id=skill_id, user=request.user)
        user_skill.delete()
        return JsonResponse({'success': True, 'message': 'Навык удален'})

    return JsonResponse({'error': 'Недопустимый запрос'}, status=400)