from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.utils import timezone
# from .validators import fone_regex
from django.contrib.auth import get_user_model
import os

from django.core.files.storage import default_storage
from PIL import Image
from io import BytesIO

# Define um validador de expressão regular para o campo de telefone (fone)
fone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Número de telefone deve estar no formato: '+999999999'. Até 15 dígitos."
)

# Define um gerenciador personalizado para o modelo de usuário (Users)
class UsuarioManager(BaseUserManager):
    # Define o uso deste gerenciador nas migrações do Django
    use_in_migrations = True

    # Método interno para criar um usuário
    def _create_user(self, email, password, **extra_fields):
        # Verifica se o email foi fornecido, caso contrário, levanta um erro
        if not email:
            raise ValueError('O e-mail é obrigatório')

        # Normaliza o email, colocando-o em letras minúsculas
        email = self.normalize_email(email)

        # Cria uma instância do usuário usando o modelo do gerenciador,
        # definindo o email e o username (que será igual ao email),
        # além dos campos adicionais fornecidos em **extra_fields
        user = self.model(email=email, username=email, **extra_fields)

        # Define a senha do usuário usando o método set_password fornecido pelo Django
        user.set_password(password)

        # Salva o usuário no banco de dados usando o método save fornecido pelo Django
        user.save(using=self._db)

        # Retorna o usuário criado
        return user

    # Método para criar um usuário normal (não superusuário)
    def create_user(self, email, password=None, **extra_fields):
        # Define os campos extras padrão, como "is_superuser" para False
        extra_fields.setdefault('is_superuser', False)

        # Chama o método _create_user para criar o usuário, fornecendo email,
        # senha e outros campos extras como argumentos
        return self._create_user(email, password, **extra_fields)

    # Método para criar um superusuário
    def create_superuser(self, email, password, **extra_fields):
        # Define os campos extras padrão para um superusuário,
        # como "is_superuser" e "is_staff" para True
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        # Verifica se o campo "is_superuser" foi definido corretamente como True,
        # caso contrário, levanta um erro
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True')

        # Verifica se o campo "is_staff" foi definido corretamente como True,
        # caso contrário, levanta um erro
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True')

        # Chama o método _create_user para criar o superusuário, fornecendo email,
        # senha e outros campos extras como argumentos
        return self._create_user(email, password, **extra_fields)
    
# Define a função para o caminho onde as fotos dos usuários serão salvas
def user_directory_path(instance, filename):
    # Obter a classe do usuário personalizado (Users) usando o get_user_model()
    User = get_user_model()

    # Obter o ID do usuário, se estiver disponível, ou usar uma string vazia
    user_id = User.objects.latest('created_at').id+1

    # O arquivo será salvo no diretório: media/users/user_<id>/<filename>
    return os.path.join('users', f'user_{user_id}', filename)

# Define o modelo Users que herda da classe AbstractUser do Django
class Users(AbstractUser):
    # Define o campo de email como um campo EmailField, com a label "E-mail" e único
    email = models.EmailField('E-mail', unique=True)

    # Define o campo de foto como um campo ImageField, com a label "Foto" e chamando a função user_directory_path para definir o caminho de armazenamento
    # foto = models.ImageField('Foto', upload_to=user_directory_path, null=True, blank=True)

    # Define o campo de fone como um campo CharField, com a label "Telefone" e tamanho máximo de 15 caracteres
    fone = models.CharField('Telefone', max_length=15, blank=True)

    # Define o campo de data de nascimento como um campo DateField, com a label "Data de Nascimento" e pode ser nulo (não obrigatório)
    data_nascimento = models.DateField('Data de Nascimento', null=True, blank=True)

    # Define o campo de foto como um campo ImageField, com a label "Foto" e chamando a função user_directory_path para definir o caminho de armazenamento
    # foto = models.ImageField('Foto', upload_to=user_directory_path, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    # Define o campo que será usado como o identificador do usuário (campo de login),
    # neste caso, usamos o campo de email como identificador único do usuário
    USERNAME_FIELD = 'email'

    # Define os campos extras que serão obrigatórios ao criar um usuário,
    # além dos campos padrão fornecidos pela classe AbstractUser
    REQUIRED_FIELDS = ['first_name', 'last_name', 'fone', 'data_nascimento']

    # Método que retorna uma representação em string do objeto Users,
    # neste caso, usamos o email como representação
    def __str__(self):
        return self.email

    # Define o gerenciador personalizado (UsuarioManager) para o modelo Users
    objects = UsuarioManager()

class Genero(models.Model):
    nome = models.CharField('Nome', max_length=50, unique=True)
    descricao = models.TextField('Descrição', blank=True, null=True)

    def __str__(self):
        return self.nome

class Profile(models.Model):
    # Relação um-para-um com o modelo Users.
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='profile')
    # Define o campo de foto como um campo ImageField, com a label "Foto" e chamando a função user_directory_path para definir o caminho de armazenamento
    foto = models.ImageField('Foto', upload_to=user_directory_path, null=True, blank=True)
    # Campo de biografia.
    # bio = models.TextField('Biografia', blank=True, null=True, max_length=500)

    genero = models.ForeignKey(Genero, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Gênero')

    is_paciente = models.BooleanField('Você já é paciente?', default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Salva o objeto primeiro

        if self.foto:  # Verifica se a foto foi carregada
            # Abre a imagem usando Pillow a partir do sistema de armazenamento de arquivos
            with default_storage.open(self.foto.name, 'rb') as f:
                img = Image.open(f)

                # Corta a imagem para a relação de aspecto desejada (neste caso, 1:1)
                width, height = img.size
                new_dimension = min(width, height)
                left = (width - new_dimension) / 2
                top = (height - new_dimension) / 2
                right = (width + new_dimension) / 2
                bottom = (height + new_dimension) / 2
                img = img.crop((left, top, right, bottom))

                # Redimensiona a imagem para 300x300
                output_size = (300, 300)
                img = img.resize(output_size, Image.LANCZOS)

                # Identifica o formato do arquivo de imagem. Se img.format for None, obtém a extensão do nome do arquivo
                ext = img.format
                if ext is None:
                    ext = self.foto.name.split('.')[-1]
                ext = ext.lower()

                # Salva a imagem redimensionada de volta ao sistema de armazenamento de arquivos
                with default_storage.open(self.foto.name, 'wb') as f:
                    if ext == "jpg":
                        ext = "jpeg"
                    img.save(f, format=ext)


    def __str__(self):
        return f'Profile de {self.user.get_full_name()}'

