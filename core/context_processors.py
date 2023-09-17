# core/context_processors.py
from conteudo.models import Categoria, Notificacao, Conteudo, Icone
from conteudo.forms import CategoriaForm

from usuarios.models import Genero
from usuarios.forms import UsersChangeForm, ProfileForm

from core.models import infosApp
from core.forms import infosAppForm

from django.db.models import Prefetch, Count
from django.utils import timezone

def categorias_sidebar(request):
    # Obtém a data e hora atual
    if request.user.is_authenticated:
        agora = timezone.now()
        
        # Query para buscar os conteúdos ativos e com data_publicacao <= agora
        queryset_conteudo = Conteudo.objects.filter(ativo=True, data_publicacao__lte=agora).order_by('-data_publicacao')
        
        # Query para buscar as categorias ativas e ordená-las pelo campo 'ordem'
        # Também faz o prefetch dos conteúdos ativos relacionados
        categorias = Categoria.objects.filter(ativo=True).order_by('ordem').prefetch_related(
            Prefetch('conteudo_set', queryset=queryset_conteudo)
        )
        queryset_conteudo_all = Conteudo.objects.filter(ativo=True).order_by('-data_publicacao')
        # Também faz o prefetch dos conteúdos ativos relacionados
        categorias_all = Categoria.objects.filter(ativo=True).order_by('ordem').prefetch_related(
            Prefetch('conteudo_set', queryset=queryset_conteudo_all)
        )
    else:
        return {'categorias_sidebar': {},
            'categorias_all': {}}

    return {'categorias_sidebar': categorias,
            'categorias_all': categorias_all}

def conteudos_ativos(request):
    if request.user.is_authenticated:
        agora = timezone.now()
        return {'conteudos_ativos': Conteudo.objects.filter(ativo=True, data_publicacao__lte=agora).order_by('-data_publicacao')}
    else:
        return {'conteudos_ativos': {}}
def user_details(request):
    context = {}
    
    if request.user.is_authenticated:
        context['profile'] = request.user.profile
        context['generos'] = Genero.objects.all()
        user = request.user
        context['user_form'] = UsersChangeForm(instance=user)
        context['profile_form'] = ProfileForm(instance=user.profile)
        context['notificacoes'] = Notificacao.objects.filter(usuario=request.user,lido=False).order_by('-data_hora')[:5]  # Obtém as 5 últimas notificações
        context['numero_notificacoes'] = Notificacao.objects.filter(usuario=request.user, lido=False).count()
        context['icones'] = Icone.objects.all()
        context['categoria_form'] = CategoriaForm()

    return context

def info_context(request):
    try:
        # Pegando o primeiro registro da tabela infosApp
        info = infosApp.objects.first()
    except infosApp.DoesNotExist:
        info = None

    # Retornando o contexto
    return {'info': info}