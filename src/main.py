import os
from flask import Flask
from init import db, ma, bcrypt, jwt
from controllers.cli_controller import db_bp
from controllers.auth_controller import auth_bp
from controllers.orders_controller import order_bp
from controllers.food_controller import food_bp
from marshmallow.exceptions import ValidationError


def create_app():
    app = Flask(__name__)

    @app.errorhandler(401)
    def unauthorized(err):
        return {'error': str(err)}, 401

    @app.errorhandler(405)
    def method_not_allowed(err):
        return {'error': str(err)}, 405

    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'error': str(err)}, 400

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
    app.register_blueprint(food_bp)

    return app
