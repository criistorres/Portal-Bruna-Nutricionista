from django.db import models

from django.utils import timezone
from django.utils.timesince import timesince

from django.urls import reverse
from usuarios.models import Users

# Modelo para representar a Categoria
class Categoria(models.Model):

    ICONE_CHOICES = (
        ('fa-heart', 'Coração'),
        ('fa-apple-alt', 'Maçã'),
        ('fa-dumbbell', 'Haltere'),
        ('fa-stethoscope', 'Estetoscópio'),
        ('fa-hamburger', 'Hambúrguer'),
        ('fa-leaf', 'Folha'),
        ('fa-running', 'Corrida'),
        ('fa-bicycle', 'Bicicleta'),
        ('fa-tooth', 'Dente'),
        ('fa-pills', 'Comprimidos'),
        ('fa-water', 'Água'),
        ('fa-weight', 'Peso'),
        ('fa-carrot', 'Cenoura'),
        ('fa-bed', 'Cama'),
        ('fa-solid fa-person-breastfeeding', 'Teste'),
        # Adicione mais opções conforme necessário
    )

    nome = models.CharField(max_length=100)
    # descricao = models.TextField()
    icone = models.CharField(max_length=100, choices=ICONE_CHOICES)  # Usando as opções de escolha
    ativo = models.BooleanField(default=True)
    

    def __str__(self):
        return self.nome

# Modelo para representar o Cadastro de Conteúdo
class Conteudo(models.Model):
    # Campos do modelo
    titulo = models.CharField(max_length=200)
    data_publicacao = models.DateField()
    link_video = models.CharField(max_length=1000)
    descricao = models.TextField()
    # link_url = models.CharField(max_length=50)

    # Relacionamento "muitos para um" (vários conteúdos para uma categoria)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    ativo = models.BooleanField(default=True)

    def get_absolute_url(self):
        # Supondo que você tenha uma URL chamada 'detalhe_conteudo' no arquivo urls.py do app
        return reverse('conteudo_detail', args=[str(self.id)])
    def __str__(self):
        return f"Conteudo de {self.titulo} em {self.data_publicacao}"


class Comentario(models.Model):
    conteudo = models.ForeignKey(Conteudo, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='comentarios')  # Adiciona o dono do comentário

    @property
    def get_tempo_decorrido(self):
        return timesince(self.data_publicacao, timezone.now())

    def __str__(self):
        return f"Comentário de {self.owner.username} em {self.data_publicacao}"


class Resposta(models.Model):
    texto = models.TextField()
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE, related_name='respostas')
    data_publicacao = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='respostas')  # Adiciona o dono da resposta

    def __str__(self):
        return f"Resposta de {self.owner.username} em {self.data_publicacao}"

    @property
    def get_tempo_decorrido(self):
        return timesince(self.data_publicacao, timezone.now())