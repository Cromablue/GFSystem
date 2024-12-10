from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Configurações globais
FALTAS_PERMITIDAS = 0.25  # Configurável


# ----------------------------------------
# Modelo UserProfile
# ----------------------------------------


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    telefone = models.CharField(max_length=20, blank=True)
    endereco = models.CharField(max_length=100, blank=True)
    foto = models.ImageField(upload_to='user_photos/', blank=True, null=True)
    aniversario = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True) 
    last_name = models.CharField(max_length=30, blank=True)  
    def __str__(self):
        return self.user.username

    def update_profile(self, data, files):
        """Atualiza o perfil do usuário com validações."""
        errors = []

        # Atualizar dados do usuário
        self.user.username = data.get('username', self.user.username)
        self.user.email = data.get('email', self.user.email)

        # Validações
        if not self.user.username:
            errors.append("O nome de usuário não pode estar vazio.")
        
        if User.objects.filter(username=self.user.username).exclude(pk=self.user.pk).exists():
            errors.append("Este nome de usuário já está em uso.")
        
        if User.objects.filter(email=self.user.email).exclude(pk=self.user.pk).exists():
            errors.append("Este email já está em uso.")

        if errors:
            raise ValidationError(errors)

        # Atualizar dados adicionais
        self.telefone = data.get('telefone', self.telefone)
        self.endereco = data.get('endereco', self.endereco)

        # Manter o aniversário existente se o novo valor for vazio
        aniversario_novo = data.get('aniversario')
        if aniversario_novo:  # Se um novo aniversário for fornecido
            self.aniversario = aniversario_novo

        if 'foto' in files:
            self.foto = files['foto']

        # Salvar alterações
        self.user.save()
        self.save()




# Sinal para criar automaticamente o perfil do usuário
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# ----------------------------------------
# Modelo Materia
# ----------------------------------------
class Materia(models.Model):
    DIAS_SEMANA = [
        ('SEG', 'Segunda-feira'),
        ('TER', 'Terça-feira'),
        ('QUA', 'Quarta-feira'),
        ('QUI', 'Quinta-feira'),
        ('SEX', 'Sexta-feira'),
        ('SAB', 'Sábado'),
    ]

    ANOS = [(str(ano), str(ano)) for ano in range(2000, 2100)]
    SEMESTRES = [
        ('1', '1º Semestre'),
        ('2', '2º Semestre'),
    ]

    nome = models.CharField(max_length=100)
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, related_name='materias')
    carga_horaria = models.IntegerField()
    dias_semana = models.JSONField(default=list, blank=True)
    faltas = models.IntegerField()
    anotacoes = models.TextField(default='', blank=True)
    oculto = models.BooleanField(default=False)
    finalizado = models.BooleanField(default=False)
    ano = models.CharField(max_length=4, choices=ANOS, default="2023")
    semestre = models.CharField(max_length=1, choices=SEMESTRES, default='1')

    def dias_semana_formatado(self):
        """Retorna os dias da semana formatados como string."""
        return ', '.join([dict(self.DIAS_SEMANA).get(dia, '') for dia in self.dias_semana])

    def limite_faltas(self):
        """Calcula o limite de faltas permitido (25% da carga horária)."""
        return self.carga_horaria * FALTAS_PERMITIDAS

    def percentual_usado(self):
        """Calcula o percentual de faltas já usadas em relação à carga horária total."""
        if self.carga_horaria > 0:
            return (self.faltas / self.carga_horaria) * 100
        return 0

    def percentual_faltas_usadas(self):
        """Calcula o percentual de faltas usadas em relação ao saldo permitido."""
        if self.carga_horaria > 0:
            percentual = (self.faltas / self.limite_faltas()) * 100
            return min(percentual, 100)
        return 0

    def clean(self):
        """Valida os dados do modelo antes de salvar."""
        # Valida o número de faltas
        if self.faltas < 0:
            raise ValidationError("O número de faltas não pode ser negativo.")

        # Valida a lista de dias da semana para evitar duplicatas
        if len(self.dias_semana) != len(set(self.dias_semana)):
            raise ValidationError("Dias da semana não podem ser repetidos.")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Matéria'
        verbose_name_plural = 'Matérias'
