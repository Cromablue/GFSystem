from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, MateriaForm
from .models import Materia

# Página inicial (dashboard)





def cadastro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro realizado com sucesso! Agora você pode fazer login.")
            return redirect('login')  # Redireciona para a página de login após o cadastro
        else:
            messages.error(request, "Ocorreu um erro no cadastro. Verifique os dados e tente novamente.")
    else:
        form = UserCreationForm()
    return render(request, 'cadastro.html', {'form': form})

@login_required
def dashboard(request):
    materias = Materia.objects.filter(aluno=request.user)
    return render(request, 'dashboard.html', {'materias': materias})

# Página de login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redireciona para o dashboard após o login
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Página de logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Adicionar matéria
@login_required
def adicionar_materia(request):
    if request.method == 'POST':
        form = MateriaForm(request.POST)
        if form.is_valid():
            materia = form.save(commit=False)
            materia.aluno = request.user
            materia.save()
            return redirect('dashboard')
    else:
        form = MateriaForm()
    return render(request, 'adicionar_materia.html', {'form': form})

# Editar matéria
@login_required
def editar_materia(request, pk):
    materia = get_object_or_404(Materia, pk=pk, aluno=request.user)
    if request.method == 'POST':
        form = MateriaForm(request.POST, instance=materia)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = MateriaForm(instance=materia)
    return render(request, 'editar_materia.html', {'form': form})

# Remover matéria
@login_required
def remover_materia(request, pk):
    materia = get_object_or_404(Materia, pk=pk, aluno=request.user)
    if request.method == 'POST':
        materia.delete()
        messages.success(request, "Matéria removida com sucesso!")
        return redirect('dashboard')
    return render(request, 'remover_materia.html', {'materia': materia})

@login_required
def finalizar_periodo(request):
    # Filtra as matérias do usuário logado e as exclui
    Materia.objects.filter(aluno=request.user).delete()
    return redirect('dashboard')     


def adicionar_faltas(request, id):
    materia = get_object_or_404(Materia, id=id)
    materia.faltas += 2  # Adiciona 2 faltas
    materia.save()  # Salva a alteração no banco de dados
    return redirect('dashboard')  # Redireciona de volta para a página de Dashboard