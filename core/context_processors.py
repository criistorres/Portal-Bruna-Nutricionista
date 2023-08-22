# core/context_processors.py
from conteudo.models import Categoria, Notificacao, Conteudo, Icone
from conteudo.forms import CategoriaForm
from usuarios.models import Genero
from usuarios.forms import UsersChangeForm, ProfileForm
from django.db.models import Prefetch, Count

def categorias_sidebar(request):
    # Query para buscar as categorias ativas
    # Ordena as categorias pelo campo ordem em ordem ascendente
    # Faz o prefetch dos conteúdos ativos relacionados
    categorias = Categoria.objects.filter(ativo=True).order_by('ordem').prefetch_related(
        Prefetch('conteudo_set', queryset=Conteudo.objects.filter(ativo=True))
    )

    return {'categorias_sidebar': categorias}

def conteudos_ativos(request):
    return {'conteudos_ativos': Conteudo.objects.filter(ativo=True)}

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
