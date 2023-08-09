from django.db import models

from django.utils import timezone
from django.utils.timesince import timesince

from django.urls import reverse
from usuarios.models import Users

    # ICONE_CHOICES = (
    #     ('fa-heart', 'Coração'),
    #     ('fa-apple-alt', 'Maçã'),
    #     ('fa-dumbbell', 'Haltere'),
    #     ('fa-stethoscope', 'Estetoscópio'),
    #     ('fa-hamburger', 'Hambúrguer'),
    #     ('fa-leaf', 'Folha'),
    #     ('fa-running', 'Corrida'),
    #     ('fa-bicycle', 'Bicicleta'),
    #     ('fa-tooth', 'Dente'),
    #     ('fa-pills', 'Comprimidos'),
    #     ('fa-water', 'Água'),
    #     ('fa-weight', 'Peso'),
    #     ('fa-carrot', 'Cenoura'),
    #     ('fa-bed', 'Cama'),
    #     ('fa-solid fa-person-breastfeeding', 'Teste'),
    #     # Adicione mais opções conforme necessário
    # )
# Modelo para representar a Categoria
# Novo Modelo para representar o Ícone
class Icone(models.Model):
    icone_css_class = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao

# Modelo atualizado para representar a Categoria
class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    icone = models.ForeignKey(Icone, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

# Modelo atualizado para representar o Cadastro de Conteúdo
class Conteudo(models.Model):
    titulo = models.CharField(max_length=200)
    data_publicacao = models.DateField()
    link_video = models.CharField(max_length=1000)
    descricao = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('conteudo_detail', args=[str(self.id)])
    
    def __str__(self):
        return f"Conteudo de {self.titulo} em {self.data_publicacao}"

    # Método para verificar se o conteúdo é recente
    def is_recent(self):
        delta = timezone.now().date() - self.data_publicacao
        return delta.days < 7


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