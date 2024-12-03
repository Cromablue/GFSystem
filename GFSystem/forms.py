from .models import Materia, UserProfile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

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
        
        # Define automaticamente o ano e o semestre com base no ano atual
        from datetime import datetime
        current_year = str(datetime.now().year)
        current_semester = '1' if datetime.now().month <= 6 else '2'
        self.fields['ano'].initial = current_year
        self.fields['semestre'].initial = current_semester
        
        # Oculta os campos de ano e semestre
        self.fields['ano'].widget = forms.HiddenInput()
        self.fields['semestre'].widget = forms.HiddenInput()
        
        # Se for edição, omite o campo 'anotacoes'
        if is_edit:
            self.fields['anotacoes'].widget = forms.HiddenInput()  # Oculta o campo de anotações

        
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    senha = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    pass

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de Usuário'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primeiro Nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Último Nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['telefone', 'endereco', 'aniversario', 'foto']
        widgets = {
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço'}),
            'aniversario': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }