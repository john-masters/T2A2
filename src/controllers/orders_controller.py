import os
from datetime import date
from flask import Blueprint, request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.order import Order, OrderSchema
from models.user import User
from controllers.auth_controller import check_admin

order_bp = Blueprint('order', __name__, url_prefix='/orders')

# message = Mail(
#     from_email='12849@coderacademy.edu.au',
#     to_emails='mastersjohnr@gmail.com',
#     subject='Sending with Twilio SendGrid is Fun',
#     html_content='<strong>and easy to do anywhere, even with Python</strong>'
#     )
# try:
#     sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#     response = sg.send(message)
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)
# except Exception as err:
#     print(err)

# Get all orders
@order_bp.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # If the user isn't an admin, only return their orders
    if not user.is_admin:
        stmt = db.select(Order).filter_by(user_id=user_id).order_by(Order.id)
        orders = db.session.scalars(stmt)
        return OrderSchema(many=True).dump(orders)
    # If the user is an admin, return all orders
    else:
        stmt = db.select(Order).order_by(Order.id)
        orders = db.session.scalars(stmt)
        return OrderSchema(many=True).dump(orders)

@order_bp.route('/<int:id>/', methods=['GET'])
def get_order(id):
    stmt = db.select(Order).filter_by(id=id)
    order = db.session.scalar(stmt)
    if order:
        return OrderSchema().dump(order)
    else:
        return {'error': f'Order not found with id {id}'}, 404

@order_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    order = Order(
        user_id = get_jwt_identity(),
        date = date.today(),
        price = 0
    )
    db.session.add(order)
    db.session.commit()
    return OrderSchema().dump(order), 201
