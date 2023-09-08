from ...models import Icone
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = 'Cadastra ícones automaticamente'

    def handle(self, *args, **options):
        icone_choices = [
                ('fas fa-heart', 'Coração'),
                ('fas fa-apple-alt', 'Maçã'),
                ('fas fa-dumbbell', 'Haltere'),
                ('fas fa-play', 'Play'),
                ('fas fa-hamburger', 'Hambúrguer'),
                ('fas fa-leaf', 'Folha'),
                ('fas fa-running', 'Corrida'),
                ('fas fa-bicycle', 'Bicicleta'),
                ('fas fa-tooth', 'Dente'),
                ('fas fa-pills', 'Comprimidos'),
                ('fas fa-water', 'Água'),
                ('fas fa-weight', 'Peso'),
                ('fas fa-carrot', 'Cenoura'),
                ('fas fa-bed', 'Cama'),
            # ... outras opções ...
        ]

        for choice in icone_choices:
            icone_css_class, descricao = choice
            # Verifica se o ícone já existe
            if not Icone.objects.filter(icone_css_class=icone_css_class).exists():
                Icone.objects.create(icone_css_class=icone_css_class, descricao=descricao)


        self.stdout.write(self.style.SUCCESS('Ícones cadastrados com sucesso!'))
