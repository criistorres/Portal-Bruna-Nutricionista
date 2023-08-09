# Generated by Django 4.2.4 on 2023-08-08 23:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conteudo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resposta',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respostas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='conteudo',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conteudo.categoria'),
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