"""
Django settings for portal project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

import os
import socket

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# print(BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*rj#tw3d3b=^ek3b%-w&f^uypiev7__#%5la^ce5j9v7_xairj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Obtém o nome do host
hostname = socket.gethostname()

# Obtém o endereço IP
IPAddr = socket.gethostbyname(hostname)

# ALLOWED_HOSTS = ['portalzen-dev.sa-east-1.elasticbeanstalk.com']
ALLOWED_HOSTS = [IPAddr, 'localhost', '127.0.0.1']

# Define o caminho para o seu template de email personalizado
PASSWORD_RESET_EMAIL_TEMPLATE = 'registration/password_reset_email.html'





# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'core',
    'bootstrap4',
    'stdimage',
    'usuarios',
    'conteudo',
    'crispy_forms',
    'crispy_bootstrap5',

    'storages',

    'whitenoise.runserver_nostatic'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    
]

ROOT_URLCONF = 'portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'core.context_processors.categorias_sidebar',
                'core.context_processors.user_details',
                'core.context_processors.conteudos_ativos',
                'core.context_processors.info_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


""" Conexao Mysql """
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'brunanutricionista',
#         'USER': 'torrestech',
#         'PASSWORD': 'P4rmera1914!',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }


""" Conexao Postgres Localmente """

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'brunanutricionista',
#         'USER': 'postgres',
#         'PASSWORD': 'Camilly1',
#         'HOST': 'localhost',  # ou o endereço IP do seu banco de dados
#         'PORT': '5432',  # porta padrão do PostgreSQL
#     }
# }

""" Conexao Postgres AWS """

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'zendb',
        'USER': 'torrestech',
        'PASSWORD': 'P4rmera1914!',
        'HOST': 'zendb.czcu8thpibby.sa-east-1.rds.amazonaws.com',
        'PORT': '5432'
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_URL é a URL que o Django usará para referenciar arquivos estáticos em templates ou arquivos HTML. 
# Ou seja, é o prefixo usado nas URLs dos arquivos estáticos.
# STATIC_URL = '/static/'

# STATICFILES_DIRS é uma lista de diretórios onde o Django irá procurar arquivos estáticos adicionais 
# além daqueles contidos em cada aplicativo. Neste caso, está configurado para incluir os arquivos estáticos 
# presentes no diretório 'static' na raiz do seu projeto (determinado pela variável BASE_DIR).
# STATICFILES_DIRS = [
#     BASE_DIR / "static",
# ]
# print(STATICFILES_DIRS)

# MEDIA_URL é a URL que o Django usará para referenciar arquivos de mídia (como imagens, vídeos, etc.) 
# em templates ou arquivos HTML. Semelhante ao STATIC_URL, mas para arquivos de mídia.
# MEDIA_URL = '/media/'


# STATIC_ROOT é o diretório onde o comando 'collectstatic' irá coletar todos os arquivos estáticos para 
# servir em produção. É importante que este diretório seja diferente dos diretórios listados em 
# STATICFILES_DIRS para evitar conflitos.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

# MEDIA_ROOT é o diretório onde os arquivos de mídia (enviados pelos usuários ou gerenciados pela aplicação) 
# serão armazenados. É o local físico no servidor onde os arquivos de mídia estão armazenados e acessados.
MEDIA_ROOT = BASE_DIR / 'media'


#Registra o modelo de usuário, neste caso usamos um Custom login para logar com o email
AUTH_USER_MODEL = 'usuarios.Users'

CRISPY_TEMPLATE_PACK = 'bootstrap5'
CRISPY_ALLOWED_TEMPLATE_PACK = 'bootstrap5'
# CRISPY_TEMPLATE_PREFIX = 'bootstrap4/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#smtp configuration to use the email ctorres@beautyservices.com.br
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'nutribrunasuporte@gmail.com'
# EMAIL_HOST_PASSWORD = '@12marcos'
EMAIL_HOST_PASSWORD = 'lycsjuwvitiyidpt'

"""  Integração AWS - Imagens e arquivos estaticos  """

AWS_ACCESS_KEY_ID = 'AKIA2P7BLYMG6ZQ2T5XM'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'torrestech-zen-bucket'
AWS_S3_SIGNATURE_VERSION  = 's3v4'
AWS_S3_REGION_NAME = 'us-east-2'
AWS_S3_FILE_OVERWRITE = False

# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_DEFAULT_ACL = 'public-read'
AWS_DEFAULT_ACL = None
AWS_S3_VERITY = True
AWS_QUERYSTRING_AUTH = False  # Desativar a geração de URLs assinadas
# Defina o back-end de armazenamento de arquivos do Django para usar o S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Use a URL do seu bucket S3 como MEDIA_URL
MEDIA_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
# Use a URL do seu bucket S3 como STATIC_URL
STATIC_URL = 'https://%s.s3.us-east-2.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

