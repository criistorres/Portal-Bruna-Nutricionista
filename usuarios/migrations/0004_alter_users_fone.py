# Generated by Django 4.2.4 on 2023-08-10 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_rename_gereno_genero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='fone',
            field=models.CharField(blank=True, max_length=15, verbose_name='Telefone'),
        ),
    ]