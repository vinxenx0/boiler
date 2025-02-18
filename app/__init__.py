from flask import Flask, request, session
from flask_login import LoginManager
from flask_babel import Babel
from config import Config
from app.models.database import db, init_db
from app.models.user import User
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer

mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
serializer = URLSafeTimedSerializer("your_secret_key")

babel = Babel()  # Babel debe inicializarse fuera de la función

def get_locale():
    """ Devuelve el idioma actual del usuario. """
    return session.get('lang', request.accept_languages.best_match(['en', 'es']))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar DB
    init_db(app)
    
    mail.init_app(app)

    # Configurar Babel correctamente
    babel.init_app(app, locale_selector=get_locale)

    # ✅ Registrar `get_locale()` en el contexto de Jinja con `context_processor`
    @app.context_processor
    def inject_globals():
        return {'get_locale': get_locale}

    # Configurar Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registrar Blueprints
    from app.controllers.home_controller import home_bp
    from app.controllers.auth_controller import auth_bp
    from app.api.user_api import api_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
