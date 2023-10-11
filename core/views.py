from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import re
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from conteudo.models import Categoria

from django.template.loader import render_to_string
from django.utils.html import strip_tags

""" LoginRequiredMixin é uma classe de mixin fornecida pelo Django que pode ser usada para restringir o acesso a 
    determinadas views (visualizações) somente para usuários autenticados. 
    Esse mixin é frequentemente utilizado em conjunto com as views genéricas do Django, 
    como DetailView, ListView, TemplateView, entre outras. """

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    login_url = '/users/login/'  # URL de login

    def handle_no_permission(self):
        return redirect(self.login_url)
    

class Erro404View(TemplateView):
    template_name = '404.html'


class ContatoView(TemplateView):
    template_name = 'contato.html'

    def post(self, request, *args, **kwargs):
        # Recupere os dados do formulário
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        mensagem = request.POST.get('mensagem')

        # Verifique o formato do email
        if not re.match(r'^[\w\.-]+@[\w\.-]+$', email):
            messages.add_message(request, messages.SUCCESS, 'Por favor, insira um email válido.')
            return render(request, self.template_name)

        # Renderize o template HTML com os dados do formulário
        html_message = render_to_string('email_contato.html', {'nome': nome, 'email': email, 'telefone': telefone, 'mensagem': mensagem})

        # Remova as tags HTML do corpo do email para criar uma versão de texto simples
        plain_message = strip_tags(html_message)

        # Configure e envie o email
        send_mail(
            'Contato Zen',
            plain_message,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],  # Substitua pelo endereço de email de destino
            html_message=html_message,  # Corpo HTML do email
        )
        messages.add_message(request, messages.SUCCESS, 'E-mail enviado com sucesso, assim que possível retornaremos.')
        # Redirecione para a página de contato com uma mensagem de sucesso
        return render(request, self.template_name)