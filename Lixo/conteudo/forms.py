from django import forms
from .models import Conteudo, Categoria, Comentario, Resposta

class ConteudoForm(forms.ModelForm):
    class Meta:
        model = Conteudo
        fields = ['titulo', 'data_publicacao', 'link_video', 'descricao', 'categoria', 'ativo']

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['ativo','nome','icone']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['conteudo','texto','owner']

class RespostaForm(forms.ModelForm):
    class Meta:
        model = Resposta
        fields = ['comentario','texto','owner']

