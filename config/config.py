import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, '../avikus.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

SWAGGER_URL = '/swagger'
SWAGGER_API_URL = '/static/swagger.json'

# redis
CACHE_TYPE = 'redis'
CACHE_REDIS_URL = 'redis://redis:6379'
CACHE_DEFAULT_TIMEOUT = 300  # 기본 타임아웃 시간 (예: 300초)

CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_BROKER_URL = 'redis://redis:6379/0'


