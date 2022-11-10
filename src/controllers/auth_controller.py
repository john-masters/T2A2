from datetime import timedelta
from flask import Blueprint, request, abort
from sqlalchemy.exc import IntegrityError
from init import db, bcrypt
from models.user import User, UserSchema
from models.order import Order
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
    
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/signup/', methods=['POST'])
def auth_register():
    try:
        user = User(
           name = request.json['name'],
           email = request.json['email'],
           password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
        )
        db.session.add(user)
        db.session.commit()
        return UserSchema(exclude=['password', 'is_admin']).dump(user), 201
    except IntegrityError:
        return {'error': 'Email address already exists'}, 409

@auth_bp.route('/signin/', methods=['POST'])
def auth_login():
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return {'email': user.email, 'token': token, 'is_admin': user.is_admin}
    else:
        return {'error': 'Invalid credentials'}, 401

# Get list of all users (admin only)
@auth_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    check_admin()
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return UserSchema(many=True).dump(users)

# Delete users (admin only)

def check_admin():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not user.is_admin:
        abort(401)

# Check if the user_id for the order matches the user_id of the user making the request
def check_owner():
    user_id = get_jwt_identity()
    order_id = request.view_args['id']
    stmt = db.select(Order).filter_by(id=order_id)
    order = db.session.scalar(stmt)
    if order.user_id != int(user_id):
        abort(401)
