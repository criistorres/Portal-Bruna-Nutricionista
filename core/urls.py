from django.urls import path, include
from django.contrib.auth.views import LogoutView
# from core.views import logout_view, festa_junina
from .views import IndexView
from . import views

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    # path('sidebar/', views.sidebar, name='sidebar'),
]
