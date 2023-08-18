from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, View
from .models import Conteudo, Comentario, Resposta, Categoria, Notificacao, Icone
from django.views.generic import TemplateView,ListView
from usuarios.models import Users

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin 

from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from .forms import ConteudoForm, CategoriaForm

from django.http import JsonResponse
from django.views.generic.edit import UpdateView

    
class ResponderComentarioView(LoginRequiredMixin, View):
    def post(self, request, conteudo_pk, comentario_pk, usuario_pk):
        comentario = get_object_or_404(Comentario, pk=comentario_pk)
        resposta_texto = request.POST.get('resposta_texto')
        owner_id = Users.objects.get(pk=usuario_pk)

        if resposta_texto:
            # Aqui, você cria a resposta e armazena o objeto resposta retornado na variável "resposta"
            resposta = Resposta.objects.create(comentario=comentario, texto=resposta_texto, owner_id=owner_id.pk)
            
            # Criando a notificação para o autor do comentário original:
            notificacao = Notificacao(usuario=comentario.owner, resposta=resposta, gerador=resposta.owner)
            notificacao.save()

            messages.success(request, 'Resposta publicada com sucesso!')

        return redirect('conteudo:conteudo_detail', pk=conteudo_pk)

class Erro404View(TemplateView):
    template_name = '404.html'

class MarcarNotificacoesComoLidasView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            notificacoes = Notificacao.objects.filter(usuario=request.user, lido=False)
            for notificacao in notificacoes:
                notificacao.marcar_como_lido()
        # Redirecione para a página que você quiser após marcar as notificações como lidas, por exemplo, a página de notificações.
        return redirect('index')
    

        
class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'modal_cadastro_categoria.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Módulo criado com sucesso!')
        return response
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Ocorreu um erro no processamento do seu cadastro, revise o formulário!')
        return redirect('index')
    
    def get_success_url(self):
        # Redireciona para a página de detalhes do conteúdo criado
        return reverse('index')
    
    def get(self, request, *args, **kwargs):
        context = {
            'categoria_form': CategoriaForm(),  # Usando o formulário padrão
            'categorias': Categoria.objects.all(),  # Adicionando categorias ao contexto
            'icones': Icone.objects.all()
        }
        return render(request, self.template_name, context)


class ConteudoCreateView(LoginRequiredMixin, CreateView):
    model = Conteudo
    form_class = ConteudoForm
    template_name = 'modal_cadastro_conteudo.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Conteúdo criado com sucesso!')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Ocorreu um erro no processamento do seu cadastro, revise o formulário!')
        return redirect('index')

    def get_success_url(self):
        # Redireciona para a página de detalhes do conteúdo criado
        return reverse('conteudo:conteudo_detail', args=[self.object.id])

    def get(self, request, *args, **kwargs):
        context = {
            'conteudo_form': ConteudoForm(),  # Usando o formulário padrão
            'categorias': Categoria.objects.all()  # Adicionando categorias ao contexto
        }
        return render(request, self.template_name, context)

class ConteudoListView(ListView):
    model = Conteudo
    template_name = 'conteudos.html'
    context_object_name = 'conteudos'
    # paginate_by = 10  # Adicione isto para paginar, se quiser

    
class ConteudoDetailView(LoginRequiredMixin, DetailView):
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
    
    
class ConteudoUpdateView(LoginRequiredMixin, UpdateView):
    model = Conteudo
    form_class = ConteudoForm
    template_name = 'modal_edita_conteudo.html'
    success_url = reverse_lazy('conteudos.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conteudo_form'] = ConteudoForm(instance=self.object)  # Carrega o objeto existente no formulário
        context['categorias'] = Categoria.objects.all()
        context['conteudo'] = self.object
        context['id_conteudo'] = context['conteudo'].pk
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()  # Obtenha o objeto baseado no pk fornecido na URL
        context = self.get_context_data(object=self.object)
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        id_conteudo = request.POST.get('idConteudoValue', None)
        
        try:
            # Obtém o objeto baseado no id_conteudo
            self.object = Conteudo.objects.get(pk=id_conteudo)
        except Conteudo.DoesNotExist:
            messages.error(self.request, 'Erro: Conteúdo não encontrado.')
            return redirect('index')

        # Instancia o formulário
        form = self.form_class(request.POST, request.FILES, instance=self.object)

        # Verifica se o formulário é válido
        if form.is_valid():
            # Salva as alterações no objeto
            form.save()
            
            messages.success(self.request, 'Conteúdo atualizado com sucesso!')
            return redirect(self.get_success_url())
        else:
            # Se o formulário não for válido, retorne o formulário com os erros
            messages.error(self.request, 'Ocorreu um erro na atualização. Por favor, revise o formulário!')
            return redirect('index')  # ou qualquer outra URL padrão que você desejar

    def get_success_url(self):
        # Redireciona para a página de detalhes do conteúdo atualizado
        return reverse('conteudo:conteudo_list')