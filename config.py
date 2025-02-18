import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "your_secret_key"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    BABEL_DEFAULT_LOCALE = 'es'  # Idioma por defecto
    BABEL_TRANSLATION_DIRECTORIES = 'app/translations'
    
    # Configuración de Flask-Mail (Usar variables de entorno)
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "tuemail@gmail.com")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "tupassword")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "tuemail@gmail.com")

