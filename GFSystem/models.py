from django.db import models


class aluno (models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    senha = models.CharField(max_length=50)
    def __str__(self):
        return self.nome


class materia (models.Model):
    nome = models.CharField(max_length=100) 
    carga_horaria = models.IntegerField() #o aluno vai inserir no formulario da pagina web
    dias_semana = models.CharField(max_length=30)
    notes = models.TextField(max_length=1000)
    def __str__(self):
        return self.nome