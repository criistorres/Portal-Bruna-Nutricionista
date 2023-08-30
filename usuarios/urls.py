from django.urls import path
from .views import CadastroView, LoginView, LogoutView, CustomPasswordResetConfirmView, UserProfileView
from .views_usuarios import UserListView, UserUpdateView, DeleteUserView

from django.contrib.auth import views as auth_views

# app_name = 'usuarios'

urlpatterns = [
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', UserProfileView.as_view(), name='profile_update'),

    
    path('password_reset/', auth_views.PasswordResetView.as_view(
            template_name='password_reset.html'), 
            name='password_reset'),  
            
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'), 
            name='password_reset_done'),

    path('password_reset_complete/', 
         auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'), 
            name='password_reset_complete'),    
                
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('usuarios/', UserListView.as_view(), name='usuarios_list'),
    path('editar/<int:pk>/', UserUpdateView.as_view(), name='usuarios_edit'),
    path('delete/<int:pk>/', DeleteUserView.as_view(), name='usuarios_delete'),

]