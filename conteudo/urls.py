from django.urls import path
from . import views
from .views import ConteudoCreateView, CategoriaCreateView, ConteudoListView, ConteudoUpdateView, CategoriaListView,CategoriaUpdateView,DeleteCategoriaView
# from .views import conteudo_detail_view

app_name = 'conteudo'

urlpatterns = [
    path('<int:pk>/', views.ConteudoDetailView.as_view(), name='conteudo_detail'),
    path('<int:conteudo_pk>/responder/<int:comentario_pk>/<int:usuario_pk>/', views.ResponderComentarioView.as_view(), name='responder_comentario'),
    path('', views.MarcarNotificacoesComoLidasView.as_view(), name='marcar_notificacoes_como_lidas'),
    path('cadastrar-conteudo/', ConteudoCreateView.as_view(), name='cadastrar_conteudo'),
    path('cadastrar-categoria/', CategoriaCreateView.as_view(), name='cadastrar_categoria'),
    path('conteudos/', ConteudoListView.as_view(), name='conteudo_list'),
    path('editar_conteudo/<int:pk>/', ConteudoUpdateView.as_view(), name='editar_conteudo'),
    path('delete/conteudo/<int:pk>/', views.DeleteConteudoView.as_view(), name='delete_conteudo'),

    path('categorias/', CategoriaListView.as_view(), name='categoria_list'),
    path('editar_categoria/<int:pk>/', CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('delete/categoria/<int:pk>/', views.DeleteCategoriaView.as_view(), name='delete_categoria'),
    path('search/', views.ConteudoSearchView.as_view(), name='conteudo_search'),

]
