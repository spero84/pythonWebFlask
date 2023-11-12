from homework import create_app
import os

# config_name = os.environ.get("CONFIG")
config_name = 'local'
# app = create_app(config_name)
app, celery = create_app(config_name)
app.app_context().push()


