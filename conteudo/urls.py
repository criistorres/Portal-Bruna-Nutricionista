from django.urls import path
from . import views
# from .views import conteudo_detail_view

app_name = 'conteudo'

urlpatterns = [
    path('<int:pk>/', views.ConteudoDetailView.as_view(), name='conteudo_detail'),
    path('<int:conteudo_pk>/responder/<int:comentario_pk>/<int:usuario_pk>/', views.ResponderComentarioView.as_view(), name='responder_comentario'),
    # path('<int:conteudo_pk>/comentar/<int:comentario_pk>/<int:usuario_pk>/', views.CriarComentarioView.as_view(), name='criar_comentario'),
]
