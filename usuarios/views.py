from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from usuarios.models import Users
from django.contrib.auth import authenticate, login as login_django
from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import render, redirect

from django.contrib.auth import logout

from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy

from .forms import PasswordResetConfirmForm
from django.views.generic import TemplateView
from .models import Genero
from django.contrib import messages
from .forms import UsersChangeForm, ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.core.mail import send_mail
from django.conf import settings

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_form'] = UsersChangeForm(instance=user)
        context['profile_form'] = ProfileForm(instance=user.profile)
        context['generos'] = Genero.objects.all()
        return context

    def post(self, request):
        user = self.request.user
        user_form = UsersChangeForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Alterações salvas com sucesso.")
            return render(request, self.template_name)
        else:
            errors = {}  # Aqui você pode consolidar os erros dos formulários em um dicionário
            errors.update(user_form.errors)
            errors.update(profile_form.errors)
            for field_errors in errors.values():
                for error in field_errors:
                    messages.error(request, error)
            return render(request, self.template_name)
        
class CadastroView(View):
    template_name = 'cadastro.html'

    def get(self, request):
        messages.add_message(request, messages.INFO, "Ola, Ainda estamos em fase de testes, paciencia..")
        return render(request, self.template_name)

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('userpassword')
        password2 = request.POST.get('userpassword2')
        fone = request.POST.get('fone')
        birthdate = request.POST.get('birthdate')
        foto = request.FILES.get('foto')

        if password == password2:
            user = Users.objects.filter(email=email).first()
            if user:
                messages.add_message(request, messages.ERROR, "Já existe um cadastro com este e-mail!")
                return render(request, self.template_name)
            else:
                user = Users.objects.create_user(email=email, 
                                                        password=password, 
                                                        fone=fone, 
                                                        first_name=first_name, 
                                                        last_name=last_name,
                                                        data_nascimento=birthdate)
                # Atualize a foto no perfil se ela existir
                if foto:
                    user.profile.foto = foto
                    user.profile.save()

                # Envie o e-mail de boas-vindas
                subject = 'Bem-vindo ao Zen'
                message = 'Mensagem de boas-vindas aqui.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [email]
                
                send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=render_to_string('email_boas_vindas.html', {'first_name': first_name}))

                messages.add_message(request, messages.SUCCESS, "Cadastro realizado! Enviamos um e-mail para você.")
                return render(request, 'login.html')
        else:
            messages.add_message(request, messages.ERROR, "As senhas não coincidem, tente novamente!")
            return render(request, self.template_name)
    
class LoginView(View):
    def get(self, request):
        # Retorna o template de login para exibir o formulário
        return render(request, 'login.html')

    def post(self, request):
        # Obtém o e-mail e a senha enviados pelo formulário de login
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Verifica se as credenciais são válidas, autenticando o usuário
        user = authenticate(email=email, password=password)

        if user:
            # Se as credenciais são válidas, faz o login do usuário na sessão do Django
            login_django(request, user)
            messages.add_message(request, messages.SUCCESS, 'Seja bem vindo (a) ao ZEN!', extra_tags='personalizado')
            # Redireciona para a página inicial (index.html) após o login bem-sucedido
            return redirect( "index")
        else:
            # Se as credenciais são inválidas, retorna uma resposta com a mensagem de erro
            messages.add_message(request, messages.ERROR, "Ops, email ou senha incorretos, tente novamente! 😞")
            return render(request, 'login.html')
    
class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('login')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = PasswordResetConfirmForm
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'password_reset_confirm.html'