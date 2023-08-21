from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('conteudo/', include('conteudo.urls', namespace='conteudo')),  # Urls do app conteudo
    path('users/', include('usuarios.urls', namespace='usuarios')), # Urls do app usuarios
    path('', include('core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
