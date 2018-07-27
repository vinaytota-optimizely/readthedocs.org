import os
import json

from .base import CommunityBaseSettings


class EnvironmentSettings(CommunityBaseSettings):

    """Settings for local development"""

    DEBUG = os.environ.get('DEBUG') == 'true'
    ALLOW_PRIVATE_REPOS = os.environ['ALLOW_PRIVATE_REPOS'] == 'true'
    PRODUCTION_DOMAIN = os.environ['PROD_HOST']
    WEBHOOK_DOMAIN = os.environ['WEBHOOK_HOST']
    WEBSOCKET_HOST = os.environ['WEBSOCKET_HOST']
    DEFAULT_PRIVACY_LEVEL = os.environ['DEFAULT_PRIVACY_LEVEL']
    PUBLIC_API_URL = PRODUCTION_DOMAIN
    CSRF_TRUSTED_ORIGINS = [PRODUCTION_DOMAIN]

    @property
    def DATABASES(self):  # noqa
        return {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': os.environ['DB_NAME'],
                'USER': os.environ['DB_USER'],
                'PASSWORD': os.environ['DB_PASS'],
                'HOST': os.environ['DB_HOST'],
                'PORT': os.environ['DB_PORT']
            }
        }

    DONT_HIT_DB = False

    ACCOUNT_EMAIL_VERIFICATION = 'none'
    SESSION_COOKIE_DOMAIN = None
    CACHE_BACKEND = 'dummy://'

    SLUMBER_USERNAME = os.environ['SLUMBER_USER']
    SLUMBER_PASSWORD = os.environ['SLUMBER_PASS']  # noqa: ignore dodgy check
    SLUMBER_API_HOST = os.environ['SLUMBER_HOST']

    # Redis setup.
    REDIS_HOST = os.environ['REDIS_HOST']
    REDIS_PORT = os.environ['REDIS_PORT']
    REDIS_ADDRESS = '{}:{}'.format(REDIS_HOST, REDIS_PORT)
    BROKER_URL = 'redis://{}/0'.format(REDIS_ADDRESS)
    CELERY_RESULT_BACKEND = BROKER_URL
    CELERY_ALWAYS_EAGER = os.environ.get('ASYNC_TASKS') != 'true'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_IGNORE_RESULT = False

    # Elastic Search setup.
    ES_HOSTS = json.loads(os.environ['ES_HOSTS'])
    ES_DEFAULT_NUM_REPLICAS = 0
    ES_DEFAULT_NUM_SHARDS = 5
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
    }

    # Mail settings
    # Whether or not to actually use the default email backend.
    if os.environ.get('ENABLE_EMAILS') != 'true':
        EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    DEFAULT_FROM_EMAIL = os.environ.get('FROM_EMAIL')
    EMAIL_HOST = os.environ.get('EMAIL_HOST')
    EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

    # File Sync -- NOTE: Must be local for single-app hosts.
    FILE_SYNCER = os.environ['FILE_SYNCER']

    # Cors origins.
    CORS_ORIGIN_WHITELIST = json.loads(os.environ['CORS_HOSTS'])

    # Social Auth config.
    @property
    def SOCIALACCOUNT_PROVIDERS(self):
        providers = super(EnvironmentSettings, self).SOCIALACCOUNT_PROVIDERS
        # This enables private repositories.
        providers['github']['SCOPE'].append('repo')
        return providers

    ACCOUNT_DEFAULT_HTTP_PROTOCOL = os.environ.get(
        'ACCOUNT_DEFAULT_HTTP_PROTOCOL'
    ) or 'http'

    # Cache backend.
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': REDIS_ADDRESS,
            'PREFIX': 'docs',
            'OPTIONS': {
                'DB': 1,
                'PARSER_CLASS': 'redis.connection.HiredisParser',
                'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
                'CONNECTION_POOL_CLASS_KWARGS': {
                    'max_connections': 5,
                    'timeout': 3,
                },
                'MAX_CONNECTIONS': 10,
                'PICKLE_VERSION': -1,
            },
        },
    }

    LOG_FORMAT = "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s"
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': LOG_FORMAT,
                'datefmt': "%d/%b/%Y %H:%M:%S"
            },
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'logging.NullHandler',
            },
            'console': {
                'level': ('INFO', 'DEBUG')[DEBUG],
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
        },
        'loggers': {
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'readthedocs.core.views.post_commit': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'core.middleware': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'restapi': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': False,
            },
            'readthedocs.projects.views.public.search': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'search': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'elasticsearch.trace': {
                'level': 'DEBUG',
                'handlers': ['console'],
            },
            '': {
                'handlers': ['console'],
                'level': 'INFO',
            }
        }
    }


EnvironmentSettings.load_settings(__name__)


if not os.environ.get('DJANGO_SETTINGS_SKIP_LOCAL', False):
    try:
        # pylint: disable=unused-wildcard-import
        from .local_settings import *  # noqa
    except ImportError:
        pass
