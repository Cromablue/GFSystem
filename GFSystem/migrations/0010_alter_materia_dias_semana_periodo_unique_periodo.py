# Generated by Django 4.2.16 on 2024-11-28 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GFSystem', '0009_alter_materia_anotacoes_periodo_materia_periodo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materia',
            name='dias_semana',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddConstraint(
            model_name='periodo',
            constraint=models.UniqueConstraint(fields=('ano', 'semestre', 'aluno'), name='unique_periodo'),
        ),
    ]
