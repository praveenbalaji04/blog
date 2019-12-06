from core import create_app
from config import app_config
from flask_login import LoginManager


flask_app = create_app(app_config)
login_manager = LoginManager()
login_manager.init_app(flask_app)
