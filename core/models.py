from django.db import models

# Create your models here.
class infosApp(models.Model):
    nome = models.CharField(max_length=100)
    nome_reduzido = models.CharField(max_length=50)
    slogan = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


