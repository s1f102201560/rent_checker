from .base import *

###############
# 初期設定周り #
###############
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG = False

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

CSRF_TRUSTED_ORIGINS = [
  ALLOWED_HOSTS,
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')



###############
# 初期設定周り #
###############
DATABASES = {
    'default': env.db()
}

##########
# その他　#
##########