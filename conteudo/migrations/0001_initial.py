# Generated by Django 4.2.4 on 2023-08-07 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('icone', models.CharField(choices=[('fa-heart', 'Coração'), ('fa-apple-alt', 'Maçã'), ('fa-dumbbell', 'Haltere'), ('fa-stethoscope', 'Estetoscópio'), ('fa-hamburger', 'Hambúrguer'), ('fa-leaf', 'Folha'), ('fa-running', 'Corrida'), ('fa-bicycle', 'Bicicleta'), ('fa-tooth', 'Dente'), ('fa-pills', 'Comprimidos'), ('fa-water', 'Água'), ('fa-weight', 'Peso'), ('fa-carrot', 'Cenoura'), ('fa-bed', 'Cama'), ('fa-solid fa-person-breastfeeding', 'Teste')], max_length=100)),
                ('ativo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
                ('data_publicacao', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Conteudo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('data_publicacao', models.DateField()),
                ('link_video', models.CharField(max_length=1000)),
                ('descricao', models.TextField()),
                ('link_url', models.CharField(max_length=50)),
                ('ativo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resposta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
                ('data_publicacao', models.DateTimeField(auto_now_add=True)),
                ('comentario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respostas', to='conteudo.comentario')),
            ],
        ),
    ]
