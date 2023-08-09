from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout

from conteudo.models import Categoria

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

