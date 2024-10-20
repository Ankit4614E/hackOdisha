from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config
import os

db = SQLAlchemy()
socketio = SocketIO()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    socketio.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'seller.login'
    login_manager.login_message_category = 'info'

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.seller import bp as seller_bp
    app.register_blueprint(seller_bp, url_prefix='/seller')

    return app
