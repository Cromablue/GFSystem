from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, MateriaForm
from .models import Materia
from django.utils import timezone


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
    # Obter ano e semestre atuais
    ano_atual = str(timezone.now().year)
    semestre_atual = '1' if timezone.now().month <= 6 else '2'
    
    # Filtra matérias que estão no semestre/ano atual
    materias = Materia.objects.filter(
        aluno=request.user,
        ano=ano_atual,
        semestre=semestre_atual
    )
    
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
        form = MateriaForm(request.POST, is_edit=True)
        if form.is_valid():
            materia = form.save(commit=False)
            materia.aluno = request.user
            materia.save()
            messages.success(request, "Matéria adicionada com sucesso!")
            return redirect('dashboard')
        else:
            messages.error(request, "Erro ao adicionar a matéria. Verifique os campos.")
    else:
        form = MateriaForm(is_edit=True)
    return render(request, 'adicionar_materia.html', {'form': form})



# Editar matéria
@login_required
def editar_materia(request, pk):
    materia = get_object_or_404(Materia, pk=pk)

    if request.method == 'POST':
        form = MateriaForm(request.POST, instance=materia, is_edit=True)  # Passa 'is_edit=True' para ocultar "Anotações"
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redireciona após salvar
    else:
        form = MateriaForm(instance=materia, is_edit=True)  # Passa 'is_edit=True' para ocultar "Anotações"

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
    if request.method == 'POST':
        ano = request.POST.get('ano')
        semestre = request.POST.get('semestre')
        
        # Filtra as matérias do usuário logado que correspondem ao ano e semestre selecionados
        materias = Materia.objects.filter(
            aluno=request.user,
            ano=ano,
            semestre=semestre
        )
        
        if materias.exists():
            # Deleta as matérias do período selecionado
            materias.delete()
            messages.success(request, f"Período {semestre}/{ano} finalizado com sucesso!")
        else:
            messages.error(request, "Nenhuma matéria encontrada para o período selecionado.")
        
        return redirect('dashboard')  # Redireciona após finalizar o período
    
    # Recupera os anos disponíveis para exibição no template
    anos = Materia.objects.filter(aluno=request.user).values_list('ano', flat=True).distinct()
    
    return render(request, 'finalizar_periodo.html', {'anos': anos})
    


def adicionar_faltas(request, id):
    materia = get_object_or_404(Materia, id=id)
    materia.faltas += 2  # Adiciona 2 faltas
    materia.save()  # Salva a alteração no banco de dados
    return redirect('dashboard')  # Redireciona de volta para a página de Dashboard

@login_required
def ver_anotacoes(request, pk):
    materia = get_object_or_404(Materia, pk=pk, aluno=request.user)
    
    if request.method == 'POST':
        anotacoes = request.POST.get('anotacoes', '').strip()
        materia.anotacoes = anotacoes
        materia.save()
        messages.success(request, "Anotações salvas com sucesso!")
        return redirect('ver_anotacoes', pk=materia.pk)

    context = {'materia': materia}
    return render(request, 'ver_anotacoes.html', context)
