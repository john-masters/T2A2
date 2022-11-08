import os
from flask import Blueprint
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from init import db
from models.order import Order, OrderSchema

order_bp = Blueprint('order', __name__, url_prefix='/orders')

message = Mail(
    from_email='12849@coderacademy.edu.au',
    to_emails='mastersjohnr@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>'
    )

try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as err:
    print(err)

@order_bp.route('/', methods=['GET'])
def get_all_orders():
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
        