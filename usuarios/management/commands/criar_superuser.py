from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from getpass import getpass

class Command(BaseCommand):
    help = 'Cria um superusuário padrão'

    def handle(self, *args, **options):
        User = get_user_model()
        email = 'nutribrunasuporte@gmail.com'
        fone = '11999532631'
        first_name = 'Administrador'
        last_name = 'Portal'

        # Verifica se o superusuário já existe
        if not User.objects.filter(username=email).exists():
            password = getpass('Digite a senha para o superusuário: ')
            User.objects.create_superuser(email=email, 
                                            password=password, 
                                            fone=fone, 
                                            first_name=first_name, 
                                            last_name=last_name)
            self.stdout.write(self.style.SUCCESS('Superusuário criado com sucesso!'))
        else:
            self.stdout.write(self.style.WARNING('Superusuário já existe. Nenhum novo superusuário foi criado.'))
