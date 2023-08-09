# core/context_processors.py
from conteudo.models import Categoria

"""
Aqui é carregada todas as categorias e conteudos
"""
def categorias_sidebar(request):
    categorias = Categoria.objects.filter(ativo=True).prefetch_related('conteudo_set').all()
    return {'categorias_sidebar': categorias}
