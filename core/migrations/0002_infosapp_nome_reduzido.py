# Generated by Django 4.2.4 on 2023-08-31 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='infosapp',
            name='nome_reduzido',
            field=models.CharField(default='Zen', max_length=100),
        ),
    ]