import os

from .base import *  # noqa


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'docs',
        'USER': os.environ.get('PG_USER'),
        'PASSWORD': os.environ.get('PG_PASSWORD'),
        'HOST': 'pg.rtd.dz.optimizely.com',
        'PORT': '',
    }
}

DEBUG = True
TEMPLATE_DEBUG = False
CELERY_ALWAYS_EAGER = False

MEDIA_URL = 'https://media.readthedocs.org/'
STATIC_URL = 'https://media.readthedocs.org/static/'
ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

BROKER_URL = 'redis://redis.dz.optimizely.com:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis.dz.optimizely.com:6379/0'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://es.rtd.dz.optimizely.com:9200',
        'INDEX_NAME': 'haystack',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'redis.dz.optimizely.com:6379',
        'PREFIX': 'docs',
        'OPTIONS': {
            'DB': 1,
            'PARSER_CLASS': 'redis.connection.HiredisParser'
        },
    },
}

# Elasticsearch settings.
ES_HOSTS = ['es.rtd.dz.optimizely.com:9200']
ES_DEFAULT_NUM_REPLICAS = 1
ES_DEFAULT_NUM_SHARDS = 2

SLUMBER_API_HOST = 'https://rtd.dz.optimizely.com'
WEBSOCKET_HOST = 'websocket.rtd.dz.optimizely.com:8088'

PRODUCTION_DOMAIN = 'rtd.dz.optimizely.com'
USE_SUBDOMAIN = True
NGINX_X_ACCEL_REDIRECT = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Lock builds for 10 minutes
REPO_LOCK_SECONDS = 300

# Don't re-confirm existing accounts
ACCOUNT_EMAIL_VERIFICATION = 'none'

FILE_SYNCER = 'readthedocs.privacy.backends.syncers.DoubleRemotePuller'

# set GitHub scope
SOCIALACCOUNT_PROVIDERS = {
    'github': {'SCOPE': ['user:email', 'read:org', 'admin:repo_hook', 'repo:status']}
}

# allauth settings
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

if not os.environ.get('DJANGO_SETTINGS_SKIP_LOCAL', False):
    try:
        from local_settings import *  # noqa
    except ImportError:
        pass
