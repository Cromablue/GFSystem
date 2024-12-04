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

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['telefone', 'endereco', 'foto', 'aniversario']

    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user

        # Atualizar os campos do User
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            profile.save()
        return profile