# Importe os módulos necessários do Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Importe os formulários personalizados para criação e edição de usuários
from .forms import UsersCreateForm, UsersChangeForm

# Importe o modelo de usuário personalizado que será registrado na administração
from .models import Users

# Defina uma nova classe de administração para o modelo Users
@admin.register(Users)
class UsersAdmin(UserAdmin):
    # Defina o formulário personalizado para adicionar novos usuários
    add_form = UsersCreateForm

    # Defina o formulário personalizado para editar usuários existentes
    form = UsersChangeForm

    # Especifique o modelo que esta classe de administração irá gerenciar
    model = Users

    # Defina quais campos do modelo serão exibidos na lista de usuários na interface de administração
    list_display = ('first_name', 'last_name', 'email', 'fone', 'is_staff')

    # Defina os grupos de campos que serão exibidos na página de edição do usuário na interface de administração
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'fone','data_nascimento','foto')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

