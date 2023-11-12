from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from flask_redis import FlaskRedis
from flask_caching import Cache
from config import config


# define db
db = SQLAlchemy()
migrate = Migrate()

cache = Cache()


def create_app():
    # creat flask app
    app = Flask(__name__)
    app.config.from_object(config)
    app.logger.info(app.config)

    # DB ORM
    db.init_app(app)

    # flask migrate
    migrate.init_app(app, db)

    redis_client = FlaskRedis(app)

    # Swagger 설정
    swagger_blueprint = get_swaggerui_blueprint(
        config.SWAGGER_URL,
        config.SWAGGER_API_URL,
        config={'app_name': "python web using flask App"}
    )

    # cache
    cache.init_app(app, config={'CACHE_TYPE': config.CACHE_TYPE,
                                'CACHE_REDIS_URL': config.CACHE_REDIS_URL})


    # blueprint
    from .views import views
    app.register_blueprint(main_view.bp)

    # redirect error page
    app.register_error_handler(404, page_not_found)

    # swagger
    app.register_blueprint(swagger_blueprint, url_prefix=config.SWAGGER_URL)

    return app




def page_not_found(e ):
    return "no page"







