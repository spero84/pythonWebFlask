import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# define baseconfig
class Config:
    DEBUG = True


class DockerConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'local.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # redis
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = 'redis://redis'
    CACHE_DEFAULT_TIMEOUT = 300  # 기본 타임아웃 시간 (예: 300초)
    # celery
    CELERY_RESULT_BACKEND = 'redis://redis'
    CELERY_BROKER_URL = 'redis://redis'
    CELERY_CONFIG = {'broker_url': 'redis://redis', 'result_backend': 'redis://redis'}
    # CELERY_CONFIG = {"broker_url": "redis://redis", "result_backend": "redis://redis"}


class LocalConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'local.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # redis
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = 'redis://localhost:6379'
    CACHE_DEFAULT_TIMEOUT = 300  # 기본 타임아웃 시간 (예: 300초)
    # celery
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_CONFIG = {'broker_url': 'redis://localhost:6379/0', 'result_backend': 'redis://localhost:6379/0'}
    # CELERY_CONFIG = {"broker_url": "redis://redis", "result_backend": "redis://redis"}


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # redis
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = 'redis://localhost:6379'
    CACHE_DEFAULT_TIMEOUT = 300  # 기본 타임아웃 시간 (예: 300초)
    # celery
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_CONFIG = {'broker_url': 'redis://localhost:6379/0', 'result_backend': 'redis://localhost:6379/0'}
    # CELERY_CONFIG = {"broker_url": "redis://redis", "result_backend": "redis://redis"}


# config mapping
config = {
    "docker": DockerConfig,
    "local": LocalConfig,
    "test": TestConfig,
}