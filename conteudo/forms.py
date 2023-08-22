from django import forms
from .models import Conteudo, Categoria, Comentario, Resposta, Icone, Notificacao

from crispy_forms.helper import FormHelper  # Importando o FormHelper do Crispy Forms
from crispy_forms.layout import Submit  # Importando o layout Submit do Crispy Forms
from django.utils import timezone


class ConteudoForm(forms.ModelForm):

    ativo = forms.BooleanField(required=False) # Pode ser utilizado NullBooleanField também
    data_publicacao = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        initial=timezone.now().date() # Define o valor padrão como a data atual
    )

    class Meta:
        model = Conteudo  # Especificando o modelo Conteudo para o formulário
        fields = ['titulo', 'data_publicacao', 'link_video', 'descricao', 'categoria', 'ativo']  # Campos do modelo que serão exibidos no formulário

    def __init__(self, *args, **kwargs):
        super(ConteudoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Inicializando o FormHelper para personalizar o formulário
        self.helper.form_method = 'post'  # Definindo o método do formulário como 'post'
        # Adicionando um botão de submit com o texto 'Cadastrar' e a classe CSS 'btn btn-primary'
        self.helper.add_input(Submit('submit', 'Cadastrar', css_class='btn btn-primary'))

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['ativo','nome','icone']

    def __init__(self, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Inicializando o FormHelper para personalizar o formulário
        self.helper.form_method = 'post'  # Definindo o método do formulário como 'post'
        # Adicionando um botão de submit com o texto 'Cadastrar' e a classe CSS 'btn btn-primary'
        self.helper.add_input(Submit('submit', 'Cadastrar', css_class='btn btn-primary'))


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
        fields = ['usuario','resposta','gerador','lido']