from flask import Flask
from modules.config import Config

def create_app(config_class=Config):
    # Load Flask and config
    app = Flask(__name__)
    app.config.from_object(Config)

    # Include the blueprint modules
    from modules.main.routes import main
    from modules.posts.routes import posts
    from modules.functions import funcs
    from modules.errors.handler import errors

    # Register blueprint
    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(funcs)
    app.register_blueprint(errors)
    return app




