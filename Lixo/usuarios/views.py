from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from usuarios.models import Users
from django.contrib.auth import authenticate, login as login_django
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect

from django.contrib.auth import logout

from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy

from .forms import PasswordResetConfirmForm

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
                                                        data_nascimento=birthdate,
                                                        foto=foto)

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
            # Redireciona para a página inicial (index.html) após o login bem-sucedido
            return render(request, "index.html")
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