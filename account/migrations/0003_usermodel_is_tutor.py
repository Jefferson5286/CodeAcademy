# Generated by Django 5.2 on 2025-04-20 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_usermodel_cpf'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='is_tutor',
            field=models.BooleanField(default=False),
        ),
    ]
