from django import forms
from .models import infosApp


class infosAppForm(forms.ModelForm):
    class Meta:
        model = infosApp
        fields = ['nome','nome_reduzido','slogan','background','logo_sem_fundo','logo_verde','logo_variacao']

