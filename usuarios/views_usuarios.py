from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from usuarios.models import Users
from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect

from django.urls import reverse, reverse_lazy

from .models import Genero, Profile, Users
from django.contrib import messages
from .forms import UsersChangeForm, ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.db.models import Q


from django.views.generic import (
    TemplateView,
    ListView,
    DeleteView, 
    CreateView,
    DetailView,
    UpdateView,
    View)

class UserListView(UserPassesTestMixin, ListView):
    model = Users
    template_name = 'usuarios_list.html'
    context_object_name = 'usuarios'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'Você não tem permissão para acessar a pagina.')
        return redirect('index')

    def get_queryset(self):
        queryset = Users.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) | 
                Q(last_name__icontains=query) | # ou quaisquer outros campos que você queira pesquisar
                Q(profile__bio__icontains=query)  # ou quaisquer outros campos que você queira pesquisar
            )
        return queryset

    # Sobrescrever o método get_context_data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuarios = context['object_list']
        context['usuarios'] = [{'user': usuario, 'perfil': Profile.objects.get(user=usuario)} for usuario in usuarios]
        context['total_usuarios'] = Users.objects.all().count()
        context['total_pacientes'] = Profile.objects.filter(is_paciente=True).count() # Substitua "seu_campo_paciente" pelo atributo ou método que você utiliza para distinguir pacientes

        return context

class UserUpdateView(UserPassesTestMixin, UpdateView):
    model = Users
    template_name = 'usuarios_edit.html'
    form_class = UsersChangeForm
    success_url = reverse_lazy('usuarios_list.html')

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'Você não tem permissão para acessar a pagina.')
        return redirect('index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verifica se já existe um formulário de perfil no contexto
        if 'profile_form' not in context:
            profile_form = ProfileForm(instance=self.object.profile)
            context['profile_form'] = profile_form
            context['usuario_editado'] = self.object.profile  # ou qualquer lógica para obter o usuário correto
        
        return context
    
    def form_valid(self, form):
        profile_form = ProfileForm(self.request.POST, instance=self.object.profile)
        if profile_form.is_valid():
            profile_form.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Redireciona para a página de detalhes do conteúdo atualizado
        return reverse('usuarios:usuarios_list')
    def form_invalid(self, form):
        response = super().form_invalid(form)

        # Adicionando uma mensagem genérica de erro
        messages.error(self.request, 'Ocorreu um erro ao atualizar o perfil. Por favor, verifique os campos e tente novamente.')

        # Você também pode percorrer os campos com erros e adicionar mensagens específicas
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Erro no campo {field}: {error}")

        return response
    
class DeleteUserView(UserPassesTestMixin, DeleteView):
    model = Users
    template_name = 'usuario_confirm_delete.html'
    success_url = reverse_lazy('usuarios:usuarios_list')

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'Você não tem permissão para deletar conteúdos.')
        return redirect('index')
    