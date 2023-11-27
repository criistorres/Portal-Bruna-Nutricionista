from django.db import models

def background_directory_path(instance, filename):
    # O arquivo será salvo no diretório: media/categorias/categoria_<id>/<filename>
    return 'background/login_{0}/{1}'.format(instance.id, filename)
# Create your models here.
class infosApp(models.Model):
    nome = models.CharField(max_length=100)
    nome_reduzido = models.CharField(max_length=50)
    slogan = models.CharField(max_length=200)
    background = models.ImageField('Background', upload_to=background_directory_path, null=True, blank=True)
    logo_sem_fundo = models.ImageField('Logo', upload_to=background_directory_path, null=True, blank=True)
    logo_verde = models.ImageField('Logo Verde', upload_to=background_directory_path, null=True, blank=True)
    logo_variacao = models.ImageField('Logo Variação', upload_to=background_directory_path, null=True, blank=True)

    def __str__(self):
        return self.nome


