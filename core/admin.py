from django.contrib import admin
from .models import infosApp
from .forms import infosAppForm

class infosAppAdmin(admin.ModelAdmin):
    form = infosAppForm


# Registre os modelos com as classes de administração personalizadas
admin.site.register(infosApp, infosAppAdmin)
