from flask import Flask
from config import Config
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app)

    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app