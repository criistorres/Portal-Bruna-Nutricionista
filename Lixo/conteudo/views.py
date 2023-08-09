from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, View
from .models import Conteudo, Comentario, Resposta, Categoria
from django.views.generic import TemplateView
from usuarios.models import Users

from django.contrib import messages


class ConteudoDetailView(DetailView):
    model = Conteudo
    template_name = 'conteudo_detail.html'
    context_object_name = 'conteudo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conteudo = context['conteudo']
        comentarios = conteudo.comentarios.all()
        context['comentarios'] = comentarios
        return context
    def post(self, request, pk):
        comentario_texto = request.POST.get('comentario_texto')
        conteudo = Conteudo.objects.get(pk=pk)
        owner_id = request.user.id

        if comentario_texto:
            comentario = Comentario.objects.create(conteudo=conteudo, texto=comentario_texto, owner_id=owner_id)
            # Associate the comentario with the conteudo
            conteudo.comentarios.add(comentario)
            messages.success(request, 'Comentário publicado com sucesso!')
        return redirect('conteudo:conteudo_detail', pk=pk)
    
    
class ResponderComentarioView(View):
    def post(self, request, conteudo_pk, comentario_pk, usuario_pk):
        comentario = get_object_or_404(Comentario, pk=comentario_pk)
        resposta_texto = request.POST.get('resposta_texto')
        owner_id = Users.objects.get(pk=usuario_pk)

        if resposta_texto:
            # Resposta.objects.create(comentario=comentario, texto=resposta_texto, owner_id=owner_id.pk)
            Resposta.objects.create(comentario=comentario, texto=resposta_texto, owner_id=owner_id.pk)
            messages.success(request, 'Resposta publicada com sucesso!')

        return redirect('conteudo:conteudo_detail', pk=conteudo_pk)

class Erro404View(TemplateView):
    template_name = '404.html'