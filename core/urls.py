from django.urls import path, include
from django.contrib.auth.views import LogoutView
# from core.views import logout_view, festa_junina
from .views import IndexView, ContatoView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contato', ContatoView.as_view(), name='contato'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)