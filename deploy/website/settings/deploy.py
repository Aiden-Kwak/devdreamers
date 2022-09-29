from .base import *

def read_secret(secret_name):

    file = open('/run/secrets/' + secret_name)
    secret = file.read()
    secret = secret.rstrip().lstrip()
    file.close()

    return secret

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# reading .env file
environ.Env.read_env(
    env_file= os.path.join(BASE_DIR, '.env')
)

SECRET_KEY = read_secret('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres_db',
        'USER': read_secret('POSTGRES_USER'),
        'PASSWORD': read_secret('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': '5432',
    }
}