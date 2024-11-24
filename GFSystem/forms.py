from .models import Materia
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = ['nome', 'carga_horaria', 'dias_semana', 'faltas']
        
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    pass