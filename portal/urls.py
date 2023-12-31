from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('conteudo/', include('conteudo.urls', namespace='conteudo')),  # Urls do app conteudo
    path('users/', include('usuarios.urls')), # Urls do app usuarios
    path('', include('core.urls')),
] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.AdminSite.site_header = 'Zen | Admin'
admin.AdminSite.site_title = 'Zona de Educação Nutricional'
admin.AdminSite.index_title = 'Administração Zen'
