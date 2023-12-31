# Generated by Django 4.2.4 on 2023-10-17 19:14

import conteudo.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('ativo', models.BooleanField(default=True)),
                ('ordem', models.PositiveIntegerField(default=0, help_text='Defina a ordem das categorias na sidebar')),
                ('descricao', models.TextField(default='')),
                ('capa', models.ImageField(blank=True, null=True, upload_to=conteudo.models.categoria_directory_path, verbose_name='Capa')),
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
            name='Icone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icone_css_class', models.CharField(max_length=100)),
                ('descricao', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Resposta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
                ('data_publicacao', models.DateTimeField(auto_now_add=True)),
                ('comentario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respostas', to='conteudo.comentario')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respostas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notificacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lido', models.BooleanField(default=False)),
                ('data_hora', models.DateTimeField(auto_now_add=True)),
                ('gerador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notificacoes_geradas', to=settings.AUTH_USER_MODEL, verbose_name='Usuário que gerou a notificação')),
                ('resposta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificacoes', to='conteudo.resposta')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificacoes_recebidas', to=settings.AUTH_USER_MODEL, verbose_name='Usuário que recebe a notificação')),
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
                ('ativo', models.BooleanField(default=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conteudo.categoria')),
            ],
        ),
        migrations.AddField(
            model_name='comentario',
            name='conteudo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='conteudo.conteudo'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='categoria',
            name='icone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conteudo.icone'),
        ),
    ]
