from flask import Flask
from flasgger import Swagger

def create_app():
    app = Flask(__name__)

    # Swagger config
    app.config["SWAGGER"] = {
        "title": "Healthspan API",
        "uiversion": 3
    }
    Swagger(app)

    # Register routes
    from .routes import bp
    app.register_blueprint(bp)

    return app
