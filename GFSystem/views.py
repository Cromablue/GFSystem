from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import datetime
from .forms import UserRegisterForm, MateriaForm
from .models import Materia
from django.contrib.auth.models import User
import re

# Página inicial
def home(request):
    return render(request, 'index.html')

# Cadastro de usuário
def cadastro(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        errors = []

        # Validações
        if not username.isalnum():
            errors.append("O nome de usuário deve conter apenas letras e números.")
        if User.objects.filter(username=username).exists():
            errors.append("Este nome de usuário já está em uso.")
        if User.objects.filter(email=email).exists():
            errors.append("Este email já está em uso.")
        if not email.endswith('.com'):
            errors.append("O email deve conter .com")
        
        password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=]).{8,}$'
        if not re.match(password_regex, password1):
            errors.append("A senha deve ter pelo menos 8 caracteres, incluir uma letra maiúscula, um número e um caractere especial.")
        if password1 != password2:
            errors.append("As senhas não coincidem.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'cadastro.html')

        User.objects.create_user(username=username, password=password1, email=email)
        messages.success(request, "Cadastro realizado com sucesso!")
        return redirect('login')

    return render(request, 'cadastro.html')

# Página de login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, "Nome de usuário ou senha incorretos.")

    return render(request, 'login.html')

# Página de logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboard
@login_required
def dashboard(request):
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

# Adicionar matéria
@login_required
def adicionar_materia(request):
    if request.method == 'POST':
        form = MateriaForm(request.POST, is_edit=True)
        if form.is_valid():
            materia = form.save(commit=False)
            materia.aluno = request.user
            materia.save()
            messages.success(request, "Matéria adicionada com sucesso!")
            return redirect('dashboard')
        messages.error(request, "Erro ao adicionar a matéria. Verifique os campos.")
    else:
        form = MateriaForm(is_edit=True)
    return render(request, 'adicionar_materia.html', {'form': form})

# Editar matéria
@login_required
def editar_materia(request, pk):
    materia = get_object_or_404(Materia, pk=pk, aluno=request.user)
    if request.method == 'POST':
        form = MateriaForm(request.POST, instance=materia, is_edit=True)
        if form.is_valid():
            form.save()
            messages.success(request, "Matéria editada com sucesso!")
            return redirect('dashboard')
    else:
        form = MateriaForm(instance=materia, is_edit=True)
    return render(request, 'editar_materia.html', {'form': form})

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

# Remover matéria
@login_required
def remover_materia(request, pk):
    materia = get_object_or_404(Materia, pk=pk, aluno=request.user)
    if request.method == 'POST':
        materia.oculto = True
        materia.save()
        messages.success(request, "Matéria removida com sucesso!")
        return redirect('dashboard')

# Lixeira
@login_required
def lixeira(request):
    materias = Materia.objects.filter(aluno=request.user, oculto=True)
    return render(request, 'lixeira.html', {'materias': materias})

# Restaurar matéria
@login_required
def restaurar_materia(request, pk):
    materia = get_object_or_404(Materia, pk=pk, aluno=request.user, oculto=True)
    materia.oculto = False
    materia.save()
    messages.success(request, "Matéria restaurada com sucesso!")
    return redirect('lixeira')

# Finalizar período
@login_required
def finalizar_periodo(request):
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

# Perfil do usuário
@login_required
def perfil(request):
    return render(request, 'perfil.html', {'user': request.user})

# Editar perfil
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')

        if not user.username or not user.email:
            messages.error(request, "Os campos 'Usuário' e 'Email' são obrigatórios.")
            return redirect('edit_profile')

        user.save()
        messages.success(request, "Perfil atualizado com sucesso!")
        return redirect('perfil')

    return render(request, 'edit_profile.html')


# Adicionar faltas
@login_required
def adicionar_faltas(request, id):
    """
    Incrementa as faltas de uma matéria específica em 2.
    """
    materia = get_object_or_404(Materia, id=id, aluno=request.user)
    materia.faltas += 2  # Adiciona 2 faltas
    materia.save()  # Salva a alteração no banco de dados
    messages.success(request, f"Faltas adicionadas com sucesso para a matéria: {materia.nome}")
    return redirect('dashboard')  # Redireciona para a página de Dashboard

@login_required
def meus_periodos(request):
    """
    Exibe as matérias finalizadas de um período específico.
    """
    if request.method == 'POST':
        ano = request.POST.get('ano')
        semestre = request.POST.get('semestre')

        # Filtrar matérias finalizadas do período selecionado
        materias = Materia.objects.filter(
            aluno=request.user,
            finalizado=True,
            semestre=semestre,
            ano=ano
        )
        if not materias.exists():
            messages.warning(request, "Nenhuma matéria encontrada para o período selecionado.")
    else:
        materias = None

    # Recuperar anos disponíveis para exibição no modal
    anos = Materia.objects.filter(aluno=request.user, finalizado=True).values_list('ano', flat=True).distinct()

    return render(request, 'meus_periodos.html', {
        'materias': materias,
        'anos': anos,
    })