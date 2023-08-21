from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from faker import Faker
from unidecode import unidecode

class Command(BaseCommand):
    help = 'Cria usuários fictícios com nomes reais para teste'

    def add_arguments(self, parser):
        parser.add_argument('--total', type=int, help='Indica o número de usuários fictícios a serem criados')

    def handle(self, *args, **options):
        User = get_user_model()
        total = options['total'] or 10  # Número padrão de usuários fictícios
        fake = Faker('pt_BR') # Para gerar nomes em português

        for i in range(total):
            first_name = fake.first_name()
            last_name = fake.last_name()
            # Removendo acentos e caracteres especiais de nome e sobrenome
            email_first_name = unidecode(first_name.lower())
            email_last_name = unidecode(last_name.lower())
            email = f'{email_first_name}.{email_last_name}@email.com'
            password = get_random_string(10) # Gere uma senha com 10 caracteres
            fone = f'1199953263{i}'
            data_nascimento = fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=90).isoformat()

            User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                fone=fone,
                data_nascimento=data_nascimento
            )
            self.stdout.write(self.style.SUCCESS(f'Usuário {first_name} {last_name} criado com sucesso!'))
