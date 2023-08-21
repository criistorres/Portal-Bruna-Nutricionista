from django.shortcuts import render, redirect, get_object_or_404
from .models import Conteudo, Comentario, Resposta, Categoria, Notificacao, Icone
from django.views.generic import (
    TemplateView,
    ListView,
    DeleteView, 
    CreateView,
    DetailView,
    UpdateView,
    View)
from usuarios.models import Users
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin 
from django.urls import reverse_lazy, reverse
# from django.views.generic.edit import CreateView
from .forms import ConteudoForm, CategoriaForm
from django.http import JsonResponse
from django.db.models import Q


class Erro404View(TemplateView):
    template_name = '404.html'

""" ########### Inicio Views de Comentario e Notificações ###########"""
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



class MarcarNotificacoesComoLidasView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            notificacoes = Notificacao.objects.filter(usuario=request.user, lido=False)
            for notificacao in notificacoes:
                notificacao.marcar_como_lido()
        # Redirecione para a página que você quiser após marcar as notificações como lidas, por exemplo, a página de notificações.
        return redirect('index')
    
""" ########### Fim Views de Comentario e Notificações ###########"""


""" ########### Inicio Views de Categoria ###########"""

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


class CategoriaListView(UserPassesTestMixin, ListView):
    model = Categoria
    template_name = 'categorias.html'
    context_object_name = 'categorias'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'Você não tem permissão para acessar a pagina de categorias.')
        return redirect('index')


class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'modal_edita_categoria.html'
    success_url = reverse_lazy('categorias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria_form'] = CategoriaForm(instance=self.object)  # Carrega o objeto existente no formulário
        context['categorias'] = Categoria.objects.all()
        context['categoria'] = self.object
        context['id_categoria'] = context['categoria'].pk
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()  # Obtenha o objeto baseado no pk fornecido na URL
        context = self.get_context_data(object=self.object)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CategoriaForm(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Categoria atualizada com sucesso.')
            return redirect(self.get_success_url())
        else:
            context = self.get_context_data(form=form)
            messages.error(request, 'Erro ao atualizar a categoria.')
            return redirect('index')  # ou qualquer outra URL padrão que você desejar
        
    def get_success_url(self):
        # Redireciona para a página de detalhes do conteúdo atualizado
        return reverse('conteudo:categoria_list')

class DeleteCategoriaView(UserPassesTestMixin, DeleteView):
    model = Categoria
    template_name = 'categoria_confirm_delete.html'
    success_url = reverse_lazy('conteudo:categoria_list')

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'Você não tem permissão para deletar módulos.')
        return redirect('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Deletar Módulo'
        context['texto_alerta'] = 'Você está prestes a deletar o seguinte módulo, LEMBRE-SE que ao deletar um módulo, os conteúdos vinculados ao mesmo serão deletados também:'
        context['categoria'] = self.object
        return context


""" ########### Fim Views Categoria ###########"""

class ConteudoCreateView(LoginRequiredMixin, CreateView):
    model = Conteudo
    form_class = ConteudoForm
    template_name = 'modal_cadastro_conteudo.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        # messages.success(self.request, 'Conteúdo criado com sucesso!')
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

class ConteudoListView(UserPassesTestMixin, ListView):
    model = Conteudo
    template_name = 'conteudos.html'
    context_object_name = 'conteudos'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'Você não tem permissão para acessar a pagina de conteúdos.')
        return redirect('index')

    def get_queryset(self):
        queryset = Conteudo.objects.all()
        query = self.request.GET.get('q')
        coluna = self.request.GET.get('coluna')
        
        if query:
            if coluna == 'titulo':
                queryset = queryset.filter(Q(titulo__icontains=query))
            elif coluna == 'descricao':
                queryset = queryset.filter(Q(descricao__icontains=query))
            elif coluna == 'categoria':
                queryset = queryset.filter(Q(categoria__nome__icontains=query))

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all().prefetch_related('conteudo_set')
        return context
    
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
    
    
class ConteudoUpdateView(UserPassesTestMixin, UpdateView):
    model = Conteudo
    form_class = ConteudoForm
    template_name = 'modal_edita_conteudo.html'
    success_url = reverse_lazy('conteudos.html')

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'Você não tem permissão para acessar a pagina.')
        return redirect('index')

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
            
            # messages.success(self.request, 'Conteúdo atualizado com sucesso!')
            return redirect(self.get_success_url())
        else:
            # Se o formulário não for válido, retorne o formulário com os erros
            messages.error(self.request, 'Ocorreu um erro na atualização. Por favor, revise o formulário!')
            return redirect('index')  # ou qualquer outra URL padrão que você desejar

    def get_success_url(self):
        # Redireciona para a página de detalhes do conteúdo atualizado
        return reverse('conteudo:conteudo_list')
    

class DeleteConteudoView(UserPassesTestMixin, DeleteView):
    model = Conteudo
    template_name = 'conteudo_confirm_delete.html'
    success_url = reverse_lazy('conteudo:conteudo_list')

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'Você não tem permissão para deletar conteúdos.')
        return redirect('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Deletar Conteúdo'
        context['texto_alerta'] = 'Você está prestes a deletar o seguinte conteúdo:'
        context['conteudo'] = self.object
        return context