from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
socketio = SocketIO()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    socketio.init_app(app)
    login_manager.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.seller import bp as seller_bp
    app.register_blueprint(seller_bp, url_prefix='/seller')

    return app
