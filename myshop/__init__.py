# myshop/__init__.py

import os
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_dance.contrib.google import make_google_blueprint
from dotenv import load_dotenv

from .models import db, User
from .config import Config

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    load_dotenv()
    print(f"GOOGLE_OAUTH_CLIENT_ID: {os.getenv('GOOGLE_OAUTH_CLIENT_ID')}")
    print(f"GOOGLE_OAUTH_CLIENT_SECRET: {os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')}")
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # extensiones
    db.init_app(app)
    Migrate(app, db)
    login_manager.init_app(app)

    # OAuth Google
    google_bp = make_google_blueprint(
        client_id=app.config["GOOGLE_OAUTH_CLIENT_ID"],
        client_secret=app.config["GOOGLE_OAUTH_CLIENT_SECRET"],
        scope=["profile","email"],
        redirect_to="auth.google_login"
    )
    app.register_blueprint(google_bp, url_prefix="/login")

    # user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # registrar blueprints
    from myshop.auth.routes    import auth
    from myshop.main.routes    import main
    from myshop.products.routes import products

    app.register_blueprint(auth,     url_prefix="/auth")
    app.register_blueprint(main)               # rutas “/”, “/popular”, etc.
    app.register_blueprint(products, url_prefix="/categoria")

    return app
