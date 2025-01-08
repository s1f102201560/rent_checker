from .base import *

###############
# 初期設定周り #
###############
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG = True

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'http://localhost',
]

DATABASES = {
    'default': env.db()
}

##########
# その他　#
##########