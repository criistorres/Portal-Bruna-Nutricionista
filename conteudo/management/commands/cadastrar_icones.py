from ...models import Icone
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = 'Cadastra ícones automaticamente'

    def handle(self, *args, **options):
        icone_choices = [
                ('fa-heart', 'Coração'),
                ('fa-apple-alt', 'Maçã'),
                ('fa-dumbbell', 'Haltere'),
                ('fa-stethoscope', 'Estetoscópio'),
                ('fa-hamburger', 'Hambúrguer'),
                ('fa-leaf', 'Folha'),
                ('fa-running', 'Corrida'),
                ('fa-bicycle', 'Bicicleta'),
                ('fa-tooth', 'Dente'),
                ('fa-pills', 'Comprimidos'),
                ('fa-water', 'Água'),
                ('fa-weight', 'Peso'),
                ('fa-carrot', 'Cenoura'),
                ('fa-bed', 'Cama'),
            # ... outras opções ...
        ]

        for choice in icone_choices:
            icone_css_class, descricao = choice
            # Verifica se o ícone já existe
            if not Icone.objects.filter(icone_css_class=icone_css_class).exists():
                Icone.objects.create(icone_css_class=icone_css_class, descricao=descricao)


        self.stdout.write(self.style.SUCCESS('Ícones cadastrados com sucesso!'))
