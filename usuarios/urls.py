from django.urls import path
from .views import CadastroView, LoginView, LogoutView, CustomPasswordResetConfirmView

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    
    path('password_reset/', auth_views.PasswordResetView.as_view(
            template_name='password_reset.html'), 
            name='password_reset'),  # URL de redefinição de senha
            
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'), 
            name='password_reset_done'),

    # path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    #         template_name='password_reset_confirm.html'), 
    #         name='password_reset_confirm'),

    path('password_reset_complete/', 
         auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'), 
            name='password_reset_complete'),    
                
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),  # URL de redefinição de senha
    # path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]