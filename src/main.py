import os
from flask import Flask
from init import db, ma, bcrypt, jwt
from controllers.cli_controller import db_bp
from controllers.auth_controller import auth_bp
from controllers.orders_controller import order_bp


def create_app():
    app = Flask(__name__)

    app.config['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @app.route('/')
    def index():
        return 'Hello World'

    app.register_blueprint(db_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(order_bp)

    return app
