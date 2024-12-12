from .models import Materia, UserProfile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import re

from datetime import datetime
from django import forms
from .models import Materia

class MateriaForm(forms.ModelForm):
    DIAS_SEMANA = Materia.DIAS_SEMANA

    # Campo personalizado para seleção dinâmica de dias
    dias_semana = forms.MultipleChoiceField(
        choices=DIAS_SEMANA,
        widget=forms.CheckboxSelectMultiple,
        label="Dias da Semana",
    )

    class Meta:
        model = Materia
        fields = ['nome', 'carga_horaria', 'faltas', 'dias_semana', 'anotacoes', 'ano', 'semestre']

    def __init__(self, *args, **kwargs):
        # Recebe o parâmetro 'is_edit' para saber se estamos na edição ou criação
        is_edit = kwargs.pop('is_edit', False)
        super(MateriaForm, self).__init__(*args, **kwargs)

        # Define valores iniciais para ano e semestre
        current_year = str(datetime.now().year)
        current_semester = '1' if datetime.now().month <= 6 else '2'
        self.fields['ano'].initial = current_year
        self.fields['semestre'].initial = current_semester

        # Campos ocultos para ano e semestre
        self.fields['ano'].widget = forms.HiddenInput()
        self.fields['semestre'].widget = forms.HiddenInput()

        # Define os campos como opcionais para evitar erros de validação
        self.fields['ano'].required = False
        self.fields['semestre'].required = False

        # Se for edição, omite o campo 'anotacoes'
        if is_edit:
            self.fields['anotacoes'].widget = forms.HiddenInput()  # Oculta o campo de anotações

    def clean_ano(self):
        """Define um valor padrão para o campo ano, caso esteja vazio."""
        ano = self.cleaned_data.get('ano')
        if not ano:
            ano = str(datetime.now().year)
        return ano

    def clean_semestre(self):
        """Define um valor padrão para o campo semestre, caso esteja vazio."""
        semestre = self.cleaned_data.get('semestre')
        if not semestre:
            semestre = '1' if datetime.now().month <= 6 else '2'
        return semestre


        
class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Senha")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmação de Senha")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        errors = []

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
            raise forms.ValidationError(errors)

        return cleaned_data

class UserLoginForm(AuthenticationForm):
    pass

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['telefone', 'endereco', 'foto', 'aniversario', 'first_name', 'last_name']  # Adicione os campos aqui

    username = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=254, required=False) 
    telefone = forms.CharField(max_length=20, required=False)
    aniversario = forms.DateField(required=False)

    def __init__(self, *args, **kwargs):
        
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError("O nome de usuário não pode estar vazio.")
        if User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("Este email já está em uso.")
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user

        # Atualizar os campos do User
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        
        # Salvar os campos adicionais no perfil
        profile.first_name = self.cleaned_data['first_name']  # Salvar primeiro nome
        profile.last_name = self.cleaned_data['last_name']    # Salvar último nome
        
        if commit:
            user.save()
            profile.save()
        
        return profile