from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from celery import Celery
from flask_caching import Cache
from config.config import config
import os


# define db
db = SQLAlchemy()
migrate = Migrate()

cache = Cache()


# def make_celery(app):
#     celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
#     celery.conf.update(app.config)
#     return celery

def make_celery(app):
    # celery = Celery(app.import_name)
    # celery.conf.update(app.config["CELERY_CONFIG"])
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app(config_key):
    # creat flask app
    app = Flask(__name__)

    app.config.from_object(config[config_key])
    app.logger.info(app.config)

    # DB ORM
    db.init_app(app)

    # flask migrate
    migrate.init_app(app, db)

    # cache
    cache.init_app(app, config={'CACHE_TYPE': app.config['CACHE_TYPE'],
                                'CACHE_REDIS_URL': app.config['CACHE_REDIS_URL']})

    from .views import views
    # blueprint
    app.register_blueprint(views.bp)

    # redirect error page / 아래는 주석 풀것!! TODO
    # app.register_error_handler(404, page_not_found)

    celery = make_celery(app)
    celery.set_default()

    # Swagger 설정
    swagger_blueprint = get_swaggerui_blueprint(
        app.config['SWAGGER_URL'],
        app.config['SWAGGER_API_URL'],
        config={'app_name': "python web using flask App"}
    )

    # swagger
    app.register_blueprint(swagger_blueprint, url_prefix=app.config['SWAGGER_URL'])

    return app
    # return app, celery


def page_not_found(e ):
    return "no page"



