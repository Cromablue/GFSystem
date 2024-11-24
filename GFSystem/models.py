from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError

class Materia(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()  # Adicionando o campo descrição
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, related_name='materias')
    carga_horaria = models.IntegerField()
    dias_semana = models.CharField(max_length=200)
    faltas = models.IntegerField()

    def limite_faltas(self):
        """Calcula o limite de faltas permitido (25% da carga horária)."""
        return self.carga_horaria * 0.25

    def percentual_usado(self):
        """Calcula o percentual de faltas já usadas."""
        return (self.faltas / self.limite_faltas()) * 100 if self.limite_faltas() > 0 else 0

    def clean(self):
        """Valida o número de faltas para garantir que não ultrapasse o limite."""
        if self.faltas > self.limite_faltas():
            raise ValidationError("O número de faltas não pode ser maior que o limite permitido.")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Matéria'
        verbose_name_plural = 'Matérias'