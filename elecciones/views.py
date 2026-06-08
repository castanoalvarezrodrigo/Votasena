import csv
import json
import secrets
from datetime import timedelta
from functools import wraps

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import (
    AprendizForm,
    CandidacyForm,
    LoginForm,
    PasswordResetConfirmForm,
    PasswordResetRequestForm,
    RegisterForm,
    VoteForm,
)
from .models import Candidacy, PasswordResetCode, Profile, Vote


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(f"{reverse('dashboard')}?show_modal=welcome")
        messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'elecciones/login.html', {'form': form})


def privacy_policy_view(request):
    return render(request, 'elecciones/privacy_policy.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        ficha = form.cleaned_data['ficha']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.profile.ficha = ficha
        user.profile.save()
        messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
        return redirect('login')

    return render(request, 'elecciones/register.html', {'form': form})


def password_reset_request(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = PasswordResetRequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        if user:
            code = f"{secrets.randbelow(1000000):06d}"
            PasswordResetCode.objects.create(user=user, code=code)
            send_mail(
                'Restablecimiento de contraseña Votasena',
                f'Código para restablecer tu contraseña: {code}\n\nSi no solicitaste este correo, ignora este mensaje.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        messages.success(request, 'Si el correo está registrado, recibirás un código para restablecer tu contraseña.')
        return redirect('password_reset_confirm')

    return render(request, 'elecciones/password_reset_request.html', {'form': form})


def password_reset_confirm(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = PasswordResetConfirmForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        code = form.cleaned_data['code']
        password1 = form.cleaned_data['password1']
        user = User.objects.filter(email=email).first()
        if not user:
            form.add_error('email', 'Correo o código inválido.')
        else:
            reset_code = (
                PasswordResetCode.objects.filter(user=user, code=code, used=False)
                .order_by('-created_at')
                .first()
            )
            if not reset_code or not reset_code.is_valid():
                form.add_error('code', 'Código inválido o expirado.')
            else:
                user.set_password(password1)
                user.save()
                reset_code.used = True
                reset_code.save()
                messages.success(request, 'Contraseña restablecida correctamente. Ahora puedes iniciar sesión.')
                return redirect('login')

    return render(request, 'elecciones/password_reset_confirm.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    profile = request.user.profile
    representantes = Candidacy.objects.filter(role=Candidacy.ROLE_REPRESENTANTE)
    voceros = Candidacy.objects.filter(role=Candidacy.ROLE_VOCERO, ficha=profile.ficha)
    subvoceros = Candidacy.objects.filter(role=Candidacy.ROLE_SUBVOCERO, ficha=profile.ficha)
    votes = Vote.objects.filter(voter=profile)
    voted_roles = {vote.role for vote in votes}

    context = {
        'profile': profile,
        'representantes': representantes,
        'voceros': voceros,
        'subvoceros': subvoceros,
        'voted_roles': voted_roles,
    }
    return render(request, 'elecciones/dashboard.html', context)


@login_required
def vote_view(request):
    if request.method != 'POST':
        return redirect('dashboard')

    profile = request.user.profile
    candidate_id = request.POST.get('candidate_id')
    candidacy = get_object_or_404(Candidacy, pk=candidate_id)

    if candidacy.role in [Candidacy.ROLE_VOCERO, Candidacy.ROLE_SUBVOCERO]:
        if candidacy.ficha != profile.ficha:
            messages.error(request, 'Solo puedes votar por aspirantes de tu ficha de aprendiz.')
            return redirect('dashboard')

    vote_exists = Vote.objects.filter(voter=profile, role=candidacy.role).exists()
    if vote_exists:
        messages.error(request, 'Ya has votado en esta categoría y no se puede cambiar tu voto.')
        return redirect('dashboard')

    Vote.objects.create(voter=profile, candidacy=candidacy, role=candidacy.role)
    messages.success(request, f'Voto registrado para {candidacy.name}.')
    return redirect('dashboard')


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return login_required(_wrapped)


@admin_required
def admin_dashboard(request):
    ficha_filter = request.GET.get('ficha', '').strip()

    role_charts = []
    for role, label in Candidacy.ROLE_CHOICES:
        candidates = (
            Candidacy.objects.filter(role=role)
            .annotate(votes=Count('vote'))
            .order_by('-votes', 'name')
        )
        role_charts.append({
            'role': label,
            'labels': json.dumps([candidate.name for candidate in candidates], ensure_ascii=False),
            'values': json.dumps([candidate.votes for candidate in candidates]),
        })

    winners = []
    for role, label in Candidacy.ROLE_CHOICES:
        winner = (
            Candidacy.objects.filter(role=role)
            .annotate(votes=Count('vote'))
            .order_by('-votes', 'name')
            .first()
        )
        winners.append({
            'role': label,
            'name': winner.name if winner else 'Sin votos',
            'votes': winner.votes if winner else 0,
        })

    winners_by_ficha = []
    if ficha_filter:
        for role, label in Candidacy.ROLE_CHOICES:
            if role == Candidacy.ROLE_REPRESENTANTE:
                continue
            query = Candidacy.objects.filter(role=role, ficha__iexact=ficha_filter)
            candidate = (
                query.annotate(votes=Count('vote'))
                .order_by('-votes', 'name')
                .first()
            )
            if candidate:
                winners_by_ficha.append({
                    'role': label,
                    'name': candidate.name,
                    'votes': candidate.votes,
                    'ficha': ficha_filter,
                })

    context = {
        'role_charts': role_charts,
        'winners': winners,
        'winners_by_ficha': winners_by_ficha,
        'ficha_filter': ficha_filter,
    }
    return render(request, 'elecciones/admin_dashboard.html', context)


@admin_required
def admin_aprendices(request):
    profiles = Profile.objects.select_related('user').all()
    username_filter = request.GET.get('username', '').strip()
    email_filter = request.GET.get('email', '').strip()
    ficha_filter = request.GET.get('ficha', '').strip()
    sort_option = request.GET.get('sort', 'username')

    if username_filter:
        profiles = profiles.filter(user__username__icontains=username_filter)
    if email_filter:
        profiles = profiles.filter(user__email__icontains=email_filter)
    if ficha_filter:
        profiles = profiles.filter(ficha__icontains=ficha_filter)

    sort_fields = {
        'username': 'user__username',
        'username_desc': '-user__username',
        'email': 'user__email',
        'email_desc': '-user__email',
        'ficha': 'ficha',
        'ficha_desc': '-ficha',
    }
    profiles = profiles.order_by(sort_fields.get(sort_option, 'user__username'))

    context = {
        'profiles': profiles,
        'username_filter': username_filter,
        'email_filter': email_filter,
        'ficha_filter': ficha_filter,
        'sort_option': sort_option,
    }
    return render(request, 'elecciones/admin_aprendices.html', context)


@admin_required
def admin_aprendiz_create(request):
    form = AprendizForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Aprendiz creado correctamente.')
        return redirect('admin_aprendices')
    return render(request, 'elecciones/admin_aprendiz_form.html', {'form': form, 'title': 'Crear aprendiz'})


@admin_required
def admin_aprendiz_edit(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    form = AprendizForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Aprendiz actualizado correctamente.')
        return redirect('admin_aprendices')
    return render(request, 'elecciones/admin_aprendiz_form.html', {'form': form, 'title': 'Editar aprendiz'})


@admin_required
def admin_aprendiz_delete(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    if request.method == 'POST':
        profile.user.delete()
        messages.success(request, 'Aprendiz eliminado correctamente.')
        return redirect('admin_aprendices')
    return render(request, 'elecciones/admin_confirm_delete.html', {
        'object': profile,
        'type': 'aprendiz',
        'cancel_url': reverse('admin_aprendices')
    })


@admin_required
def admin_candidacies(request):
    candidacies = Candidacy.objects.all()
    role_filter = request.GET.get('role', '').strip()
    ficha_filter = request.GET.get('ficha', '').strip()
    sort_option = request.GET.get('sort', 'role_name')

    if role_filter:
        candidacies = candidacies.filter(role=role_filter)
    if ficha_filter:
        candidacies = candidacies.filter(ficha__icontains=ficha_filter)

    sort_fields = {
        'role_name': ['role', 'name'],
        'role_name_desc': ['-role', '-name'],
        'ficha': ['ficha', 'name'],
        'ficha_desc': ['-ficha', '-name'],
        'name': ['name'],
        'name_desc': ['-name'],
    }
    order_fields = sort_fields.get(sort_option, ['role', 'name'])
    candidacies = candidacies.order_by(*order_fields)

    context = {
        'candidacies': candidacies,
        'role_filter': role_filter,
        'ficha_filter': ficha_filter,
        'sort_option': sort_option,
        'role_choices': Candidacy.ROLE_CHOICES,
    }
    return render(request, 'elecciones/admin_candidacies.html', context)


@admin_required
def admin_candidacy_create(request):
    form = CandidacyForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Candidato creado correctamente.')
        return redirect('admin_candidacies')
    return render(request, 'elecciones/admin_candidacy_form.html', {'form': form, 'title': 'Crear candidato'})


@admin_required
def admin_candidacy_edit(request, candidacy_id):
    candidacy = get_object_or_404(Candidacy, pk=candidacy_id)
    form = CandidacyForm(request.POST or None, instance=candidacy)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Candidato actualizado correctamente.')
        return redirect('admin_candidacies')
    return render(request, 'elecciones/admin_candidacy_form.html', {'form': form, 'title': 'Editar candidato'})


@admin_required
def admin_candidacy_delete(request, candidacy_id):
    candidacy = get_object_or_404(Candidacy, pk=candidacy_id)
    if request.method == 'POST':
        candidacy.delete()
        messages.success(request, 'Candidato eliminado correctamente.')
        return redirect('admin_candidacies')
    return render(request, 'elecciones/admin_confirm_delete.html', {
        'object': candidacy,
        'type': 'candidato',
        'cancel_url': reverse('admin_candidacies')
    })


@admin_required
def admin_votes(request):
    votes = Vote.objects.select_related('voter__user', 'candidacy').all().order_by('-created_at')
    return render(request, 'elecciones/admin_votes.html', {'votes': votes})


@admin_required
def admin_votes_export(request):
    votes = Vote.objects.select_related('voter__user', 'candidacy').all().order_by('-created_at')
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="votos_export.xls"'

    writer = csv.writer(response, delimiter='\t')
    writer.writerow(['Aprendiz', 'Candidato', 'Rol', 'Fecha'])
    for vote in votes:
        writer.writerow([
            vote.voter.user.username,
            vote.candidacy.name,
            vote.get_role_display(),
            vote.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return response


@admin_required
def admin_vote_create(request):
    form = VoteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Voto creado correctamente.')
        return redirect('admin_votes')
    return render(request, 'elecciones/admin_vote_form.html', {'form': form, 'title': 'Crear voto'})


@admin_required
def admin_vote_edit(request, vote_id):
    vote = get_object_or_404(Vote, pk=vote_id)
    form = VoteForm(request.POST or None, instance=vote)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Voto actualizado correctamente.')
        return redirect('admin_votes')
    return render(request, 'elecciones/admin_vote_form.html', {'form': form, 'title': 'Editar voto'})


@admin_required
def admin_vote_delete(request, vote_id):
    vote = get_object_or_404(Vote, pk=vote_id)
    if request.method == 'POST':
        vote.delete()
        messages.success(request, 'Voto eliminado correctamente.')
        return redirect('admin_votes')
    return render(request, 'elecciones/admin_confirm_delete.html', {
        'object': vote,
        'type': 'voto',
        'cancel_url': reverse('admin_votes')
    })
