# Generated by Django 4.2.16 on 2024-12-04 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GFSystem', '0017_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
