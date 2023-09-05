from django.db import models
from django.utils import timezone
from django.utils.timesince import timesince
from django.urls import reverse
from usuarios.models import Users

import os
from PIL import Image

class Notificacao(models.Model):
    """
    Modelo que representa uma notificação gerada quando alguém responde a um comentário.
    
    Campos:
    - usuario: O usuário que receberá a notificação (o autor do comentário original).
    - gerador: O usuário que gerou a notificação (autor da resposta).
    - resposta: A resposta que acionou a notificação.
    - lido: Indica se o usuário já leu a notificação.
    - data_hora: A data e hora em que a notificação foi gerada.
    """

    usuario = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='notificacoes_recebidas', verbose_name="Usuário que recebe a notificação")
    gerador = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, related_name='notificacoes_geradas', verbose_name="Usuário que gerou a notificação")
    resposta = models.ForeignKey('Resposta', on_delete=models.CASCADE, related_name='notificacoes')
    lido = models.BooleanField(default=False)
    data_hora = models.DateTimeField(auto_now_add=True)

    def marcar_como_lido(self):
        """
        Marca a notificação como lida.
        
        Uso:
            notificacao = Notificacao.objects.get(id=1)
            notificacao.marcar_como_lido()
        """
        self.lido = True
        self.save()

    def __str__(self):
        status = "Lida" if self.lido else "Não lida"
        gerador_username = self.gerador.username if self.gerador else 'Desconhecido'
        data_formatada = self.data_hora.strftime("%d de %B de %Y, %H:%M")
        return f"Notificação de {self.gerador.get_full_name()} para {self.usuario.get_full_name()} sobre resposta em {data_formatada}. Status: {status}"
        
class Icone(models.Model):
    """
    Representa um ícone que pode ser associado a categorias.
    
    Campos:
    - icone_css_class: Uma classe CSS que identifica o ícone visualmente.
    - descricao: Uma breve descrição do ícone.
    """
    icone_css_class = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao
    


def categoria_directory_path(instance, filename):
        # O arquivo será salvo no diretório: media/categorias/categoria_<id>/<filename>
        return os.path.join('categorias', f'categoria_{instance.id}', filename)


class Categoria(models.Model):
    """
    Representa uma categoria que pode ser associada a um conteúdo.
    
    Campos:
    - nome: O nome da categoria.
    - icone: Uma referência a um ícone associado à categoria.
    - ativo: Indica se a categoria está ativa ou não.
    """
    nome = models.CharField(max_length=100)
    icone = models.ForeignKey(Icone, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)
    ordem = models.PositiveIntegerField(default=0, help_text='Defina a ordem das categorias na sidebar')
    descricao = models.TextField(default='')
    capa = models.ImageField('Capa', upload_to=categoria_directory_path, null=True, blank=True)

    def __str__(self):
        return self.nome

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)  # Salva o objeto primeiro

    #     if self.capa:  # Verifica se a capa foi carregada
    #         img = Image.open(self.capa.path)  # Abre a imagem usando Pillow

    #         # Corta a imagem para a relação de aspecto desejada (neste caso, 1:1)
    #         width, height = img.size
    #         new_dimension = min(width, height)
    #         left = (width - new_dimension) / 2
    #         top = (height - new_dimension) / 2
    #         right = (width + new_dimension) / 2
    #         bottom = (height + new_dimension) / 2
    #         img = img.crop((left, top, right, bottom))

    #         # Redimensiona a imagem para 300x300
    #         output_size = (300, 300)
    #         img = img.resize(output_size, Image.LANCZOS)

    #         img.save(self.capa.path)  # Salva a imagem redimensionada
    



class Conteudo(models.Model):
    """
    Representa um conteúdo que pode ser visualizado pelos usuários.
    
    Campos:
    - titulo: O título do conteúdo.
    - data_publicacao: A data em que o conteúdo foi publicado.
    - link_video: Um link para um vídeo associado ao conteúdo.
    - descricao: Uma descrição detalhada do conteúdo.
    - categoria: A categoria associada ao conteúdo.
    - ativo: Indica se o conteúdo está ativo ou não.
    """
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

    @property
    def is_recent(self):
        """
        Verifica se o conteúdo foi publicado recentemente (nos últimos 7 dias).
        """
        delta = timezone.now().date() - self.data_publicacao
        return delta.days < 7
    
    @property
    def is_programado(self):
        """
        Verifica se o conteúdo foi publicado recentemente (nos últimos 7 dias).
        """
        delta = timezone.now().date() < self.data_publicacao
        return delta


class Comentario(models.Model):
    """
    Representa um comentário feito por um usuário em um conteúdo específico.
    
    Campos:
    - conteudo: O conteúdo ao qual o comentário está associado.
    - texto: O texto do comentário.
    - data_publicacao: A data e hora em que o comentário foi publicado.
    - owner: O usuário que fez o comentário.
    """
    conteudo = models.ForeignKey(Conteudo, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='comentarios')

    @property
    def get_tempo_decorrido(self):
        """
        Retorna o tempo decorrido desde a publicação do comentário.
        """
        return timesince(self.data_publicacao, timezone.now())

    def __str__(self):
        data_formatada = self.data_publicacao.strftime("%d de %B de %Y, %H:%M")
        return f"Comentário de {self.owner.username} em {data_formatada}"


class Resposta(models.Model):
    """
    Representa uma resposta a um comentário feita por um usuário.
    
    Campos:
    - texto: O texto da resposta.
    - comentario: O comentário ao qual a resposta está associada.
    - data_publicacao: A data e hora em que a resposta foi publicada.
    - owner: O usuário que fez a resposta.
    """
    texto = models.TextField()
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE, related_name='respostas')
    data_publicacao = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='respostas')

    @property
    def get_tempo_decorrido(self):
        """
        Retorna o tempo decorrido desde a publicação da resposta.
        """
        return timesince(self.data_publicacao, timezone.now())

    def __str__(self):
        data_formatada = self.data_publicacao.strftime("%d de %B de %Y, %H:%M")
        return f"Resposta de {self.owner.username} em {data_formatada}"
