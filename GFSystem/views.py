from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import datetime
from .forms import MateriaForm, UserProfileForm, UserRegistrationForm
from .models import Materia, UserProfile
import re


# Requisitos para alterar a senha:
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

# Páginas Públicas
def home(request):
    """
    Página inicial do sistema.
    """
    return render(request, 'index.html')


def cadastro(request):
    """
    Página de cadastro de usuários.
    """
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserRegistrationForm()
    return render(request, 'cadastro.html', {'form': form})


def login_view(request):
    """
    Página de login de usuários.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, "Nome de usuário ou senha incorretos.")

    return render(request, 'login.html')


def logout_view(request):
    """
    Faz logout do usuário e redireciona para a página de login.
    """
    logout(request)
    return redirect('login')


# Páginas Protegidas
@login_required
def dashboard(request):
    """
    Exibe as matérias ativas do semestre atual no Dashboard.
    """
    ano_atual = str(datetime.now().year)
    semestre_atual = '1' if datetime.now().month <= 6 else '2'

    materias = Materia.objects.filter(
        aluno=request.user,
        ano=ano_atual,
        semestre=semestre_atual,
        oculto=False,
        finalizado=False
    )
    return render(request, 'dashboard.html', {'materias': materias})


@login_required
def adicionar_materia(request):
    """
    Adiciona uma nova matéria para o usuário.
    """
    if request.method == 'POST':
        form = MateriaForm(request.POST, is_edit=True)
        if form.is_valid():
            materia = form.save(commit=False)
            materia.aluno = request.user
            materia.ano = str(datetime.now().year)
            materia.semestre = '1' if datetime.now().month <= 6 else '2'
            materia.save()
            messages.success(request, "Matéria adicionada com sucesso!")
            return redirect('dashboard')
        messages.error(request, "Erro ao adicionar a matéria. Verifique os campos.")
    else:
        form = MateriaForm(is_edit=True)
    return render(request, 'adicionar_materia.html', {'form': form})


@login_required
def editar_materia(request, pk):
    """
    Edita uma matéria existente.
    """
    materia = get_object_or_404(Materia, pk=pk, aluno=request.user)
    if request.method == 'POST':
        form = MateriaForm(request.POST, instance=materia, is_edit=True)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = MateriaForm(instance=materia, is_edit=True)
    return render(request, 'editar_materia.html', {'form': form})


@login_required
def remover_materia(request, pk):
    """
    Remove (oculta) uma matéria do dashboard.
    """
    materia = get_object_or_404(Materia, pk=pk, aluno=request.user)
    if request.method == 'POST':
        materia.oculto = True
        materia.save()
        messages.success(request, "Matéria removida com sucesso!")
        return redirect('dashboard')


def ver_anotacoes(request, pk):
    """
    Exibe e edita as anotações de uma matéria específica.
    """
    # Recupera a matéria pertencente ao usuário logado
    materia = get_object_or_404(Materia, pk=pk, aluno=request.user)
    
    if request.method == 'POST':
        # Captura as anotações enviadas pelo formulário
        anotacoes = request.POST.get('anotacoes', '').strip()
        materia.anotacoes = anotacoes
        materia.save()  # Salva as alterações no banco de dados
        messages.success(request, "Anotações salvas com sucesso!")
        return redirect('ver_anotacoes', pk=materia.pk)

    # Contexto para renderizar a página
    context = {'materia': materia}
    return render(request, 'ver_anotacoes.html', context)

@login_required
def lixeira(request):
    """
    Exibe as matérias ocultas (lixeira).
    """
    materias = Materia.objects.filter(aluno=request.user, oculto=True)
    return render(request, 'lixeira.html', {'materias': materias})


@login_required
def restaurar_materia(request, pk):
    """
    Restaura uma matéria da lixeira.
    """
    materia = get_object_or_404(Materia, pk=pk, aluno=request.user, oculto=True)
    materia.oculto = False
    materia.save()
    messages.success(request, "Matéria restaurada com sucesso!")
    return redirect('lixeira')


@login_required
def finalizar_periodo(request):
    """
    Finaliza o período atual marcando todas as matérias como finalizadas.
    """
    if request.method == 'POST':
        ano = str(datetime.now().year)
        semestre = '1' if datetime.now().month <= 6 else '2'

        materias = Materia.objects.filter(
            aluno=request.user,
            ano=ano,
            semestre=semestre
        )
        if materias.exists():
            materias.update(finalizado=True)
            messages.success(request, f"Período {semestre}/{ano} finalizado com sucesso!")
        else:
            messages.error(request, "Nenhuma matéria encontrada para o período selecionado.")
        return redirect('dashboard')

    anos = Materia.objects.filter(aluno=request.user).values_list('ano', flat=True).distinct()
    return render(request, 'finalizar_periodo.html', {'anos': anos})


@login_required
def meus_periodos(request):
    """
    Exibe as matérias finalizadas de períodos anteriores.
    """
    anos = (
        Materia.objects.filter(aluno=request.user, finalizado=True)
        .values_list('ano', flat=True)
        .distinct()
        .order_by('ano')
    )

    materias = None
    if request.method == 'POST':
        ano = request.POST.get('ano')
        semestre = request.POST.get('semestre')

        if ano and semestre:
            materias = Materia.objects.filter(
                aluno=request.user,
                finalizado=True,
                semestre=semestre,
                ano=ano,
            )
            if not materias.exists():
                messages.warning(request, "Nenhuma matéria encontrada para o período selecionado.")

    return render(request, 'meus_periodos.html', {
        'materias': materias,
        'anos': anos,
    })


# Perfil do Usuário
@login_required
def perfil(request):
    """
    Exibe as informações do perfil do usuário.
    """
    profile = request.user.profile
    return render(request, 'perfil.html', {'profile': profile})


@login_required
def edit_profile(request):
    """Permite a edição do perfil do usuário."""
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()  # Salva todos os dados corretamente
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('perfil')
    else:
        form = UserProfileForm(instance=profile, user=request.user)
    return render(request, 'edit_profile.html', {'form': form, 'profile': profile})

@login_required
def change_password(request):
    """Permite a alteração da senha do usuário."""
    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Mantém o usuário logado após a troca de senha
            messages.success(request, "Senha alterada com sucesso!")
            return redirect('perfil')
    else:
        password_form = PasswordChangeForm(request.user)

    return render(request, 'edit_senha.html', {'password_form': password_form})


@login_required
def adicionar_faltas(request, id):
    """
    Incrementa as faltas de uma matéria específica.
    """
    materia = get_object_or_404(Materia, id=id, aluno=request.user)
    materia.faltas += 2
    materia.save()
    return redirect('dashboard')