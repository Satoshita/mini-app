import os
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from .models import db
from .models import User

migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
csrf = CSRFProtect()
load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG') == '1'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        'sqlite:///people.db'   # ローカル用フォールバック
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    csrf.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .main_routes import main
    from .auth_routes import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
