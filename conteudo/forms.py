from django import forms
from .models import Conteudo, Categoria, Comentario, Resposta, Icone, Notificacao

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

class IconeForm(forms.ModelForm):
    class Meta:
        model = Icone
        fields = ['icone_css_class','descricao']

class NotificacaoForm(forms.ModelForm):
    class Meta:
        model = Notificacao
        fields = ['usuario','resposta','lido']