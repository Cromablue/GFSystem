# Generated by Django 4.2.16 on 2024-11-30 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GFSystem', '0014_alter_materia_ano_alter_materia_semestre'),
    ]

    operations = [
        migrations.AddField(
            model_name='materia',
            name='oculto',
            field=models.BooleanField(default=False),
        ),
    ]