# Generated by Django 4.2.16 on 2024-11-27 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GFSystem', '0007_alter_materia_options_alter_materia_aluno_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='materia',
            name='anotacoes',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
