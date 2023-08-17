# core/context_processors.py
from conteudo.models import Categoria, Notificacao, Conteudo, Icone
from conteudo.forms import CategoriaForm
from usuarios.models import Genero
from usuarios.forms import UsersChangeForm, ProfileForm

def categorias_sidebar(request):
    categorias = Categoria.objects.filter(ativo=True).prefetch_related('conteudo_set').all()
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
