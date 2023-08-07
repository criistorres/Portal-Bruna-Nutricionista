from django.contrib import admin
from .models import Conteudo, Categoria,Comentario,Resposta
from .forms import ConteudoForm, CategoriaForm, ComentarioForm, RespostaForm

class CadastroConteudoAdmin(admin.ModelAdmin):
    form = ConteudoForm

class CategoriaAdmin(admin.ModelAdmin):
    form = CategoriaForm

class ComentarioAdmin(admin.ModelAdmin):
    form = ComentarioForm

class RespostaAdmin(admin.ModelAdmin):
    form = RespostaForm

# Registre os modelos com as classes de administração personalizadas
admin.site.register(Conteudo, CadastroConteudoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
# Registre o modelo Comentario no painel de administração
admin.site.register(Comentario, ComentarioAdmin)

# Registre o modelo Resposta no painel de administração
admin.site.register(Resposta, RespostaAdmin)