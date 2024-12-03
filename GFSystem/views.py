from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, MateriaForm
from .models import Materia
from django.utils import timezone
import re

#fatmodels -> slin views

# Página inicial 
def home(request):
    return render(request, 'index.html') 

def cadastro(request):
    if request.method == "POST":
        # Coletando os dados do formulário
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Lista para armazenar mensagens de erro
        errors = []

        # Validação do Nome de Usuário
        if not username.isalnum():
            errors.append("O nome de usuário deve conter apenas letras e números.")
        if User.objects.filter(username=username).exists():
            errors.append("Este nome de usuário já está em uso.")

        # Validação do Email
        if User.objects.filter(email=email).exists():
            errors.append("Este email já está em uso.")
        #validando se finaliza corretamente
        if not email.endswith('.com'):
            errors.append("O email deve conter .com")

        # Validação da Senha
        password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=]).{8,}$'
        if not re.match(password_regex, password1):
            errors.append("A senha deve ter pelo menos 8 caracteres, incluir uma letra maiúscula, um número e um caractere especial.")
        
        # Confirmação da Senha
        if password1 != password2:
            errors.append("As senhas não coincidem.")
        
        # Se houver erros, retornamos para o template com os erros
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'cadastro.html')

        # Se não houver erros, criamos o usuário
        user = User.objects.create_user(username=username, password=password1)
        messages.success(request, "Cadastro realizado com sucesso!")
        return redirect('login')

    return render(request, 'cadastro.html')

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
    error_message = None  # Variável para passar o erro

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # ou o redirecionamento para onde quiser

        # Caso o usuário não exista ou a senha esteja incorreta
        error_message = "Nome de usuário ou senha incorretos."
    
    return render(request, 'login.html', {'error_message': error_message})

# Página de logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Adicionar matéria

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

def remover_materia(request, pk):
    materia = get_object_or_404(Materia, pk=pk, aluno=request.user)
    if request.method == 'POST':
        #ocultando a matéria usando a caracteristica boleana oculto
        materia.oculto = True
        materia.save()
        messages.success(request, "Matéria removida com sucesso!")
        return redirect('dashboard')
    return render(request, 'dashboard.html', {'materia': materia})


def lixeira(request):
    materias = Materia.objects.filter(aluno=request.user, oculto=True)
    return render(request, 'lixeira.html', {'materias': materias})

def restaurar_materia(request, pk):  # Adicionado o parâmetro pk
    try:
        materia = Materia.objects.get(pk=pk, aluno=request.user, oculto=True)
        materia.oculto = False
        materia.save()
        messages.success(request, "Matéria restaurada com sucesso!")
    except Materia.DoesNotExist:
        messages.error(request, "Matéria não encontrada ou você não tem permissão para restaurá-la.")
    return redirect('lixeira')


def finalizar_periodo(request):
    from datetime import datetime
    if request.method == 'POST':
        ano = str(datetime.now().year)
        semestre = '1' if datetime.now().month <= 6 else '2'
        
        # Filtra as matérias do usuário logado que correspondem ao ano e semestre selecionados
        materias = Materia.objects.filter(
            aluno=request.user,
            ano=ano,
            semestre=semestre
        )
        
        if materias.exists():
            # muda o status de todas as matérias do período selecionado para "finalizado"
            materias.update(finalizado=True)
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

def perfil(request):
    user = request.user
    # Dados adicionais, caso precise exibir mais informações
    return render(request, 'perfil.html', {'user': user})

def edit_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')

        # Validação dos campos
        if not username or not email:
            messages.error(request, "Os campos 'Usuário' e 'Email' são obrigatórios.")
            return redirect('edit_profile')

        try:
            # Atualizar informações do usuário
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('profile')  # Redirecione para a página de perfil
        except Exception as e:
            messages.error(request, f"Erro ao atualizar perfil: {str(e)}")
            return redirect('edit_profile')

    return render(request, 'edit_profile.html')  # Opcional: pode ser alterado se o modal for usado