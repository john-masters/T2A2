import os
from datetime import date
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.order import Order, OrderSchema
from models.order_item import OrderItem
from models.user import User
from controllers.auth_controller import check_admin, check_owner

order_bp = Blueprint('order', __name__, url_prefix='/orders')

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

# Get all orders except orders with the status of 'Completed' or 'Refunded'
@order_bp.route('/current/', methods=['GET'])
@jwt_required()
def get_current_orders():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # If the user isn't an admin, only return their orders
    if not user.is_admin:
        stmt = db.select(Order).filter(Order.user_id == user_id, Order.status != 'Completed', Order.status != 'Refunded').order_by(Order.id)
        orders = db.session.scalars(stmt)
        return OrderSchema(many=True).dump(orders)
    # If the user is an admin, return all orders
    else:
        stmt = db.select(Order).filter(Order.status != 'Completed', Order.status != 'Refunded').order_by(Order.id)
        orders = db.session.scalars(stmt)
        return OrderSchema(many=True).dump(orders)

# Get all orders with the status of 'Completed' or 'Refunded'
@order_bp.route('/past/', methods=['GET'])
@jwt_required()
def get_past_orders():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # If the user isn't an admin, only return their orders
    if not user.is_admin:
        stmt = db.select(Order).filter(Order.user_id == user_id, Order.status == 'Completed', Order.status == 'Refunded').order_by(Order.id)
        orders = db.session.scalars(stmt)
        return OrderSchema(many=True).dump(orders)
    # If the user is an admin, return all orders
    else:
        stmt = db.select(Order).filter(Order.status == 'Completed', Order.status == 'Refunded').order_by(Order.id)
        orders = db.session.scalars(stmt)
        return OrderSchema(many=True).dump(orders)

# Creates an order and adds the first order item to it
@order_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    # Creates the order and assigns it to the user
    order = Order(
        user_id = get_jwt_identity(),
        date = date.today()
    )
    db.session.add(order)
    db.session.commit()
    # Creates the first order item and assigns it to the order
    order_items = OrderItem(
        order_id = order.id,
        food_id = request.json['food_id'],
        quantity = request.json['quantity']
    )
    db.session.add(order_items)
    db.session.commit()

    # Loops through the order items and generates a string with all of the order details to be added to the email
    order_details = '''Order:<br></br>'''
    for order_item in order.order_items:
        order_loop = f'{order_item.quantity} * {order_item.food.name} (${order_item.food.price})<br></br>Subtotal: ${order_item.subtotal}<br></br><br></br>'
        order_details += order_loop

    # Sends an email to the user with the details of their order
    message = Mail(
        from_email='12849@coderacademy.edu.au',
        to_emails=f'{order.user.email}',
        subject=f'Your order #{order.id} has been received',
        html_content=f'''Hi, {order.user.name},<br></br><br></br>Thanks for your order!
        Your order is currently {order.status} and we will update you when this changes.
        <br></br><br></br>{order_details}Total:<br></br>${order.total_price}<br></br><br></br>
        From the Pizzeria Team!''')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as err:
        print(str(err))

    return OrderSchema().dump(order), 201

# Adds an order item to an existing order
@order_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def add_to_order(id):
    stmt = db.select(Order).filter_by(id=id)
    order = db.session.scalar(stmt)
    if order:
        order_items = OrderItem(
            order_id = order.id,
            food_id = request.json['food_id'],
            quantity = request.json['quantity']
        )
        db.session.add(order_items)
        db.session.commit()

        # Loops through the order items and generates a string with all of the order details to be added to the email
        order_details = '''Order:<br></br>'''
        for order_item in order.order_items:
            order_loop = f'{order_item.quantity} * {order_item.food.name} (${order_item.food.price})<br></br>Subtotal: ${order_item.subtotal}<br></br><br></br>'
            order_details += order_loop

        # Sends an email to the user with the updated details of their order
        message = Mail(
            from_email='12849@coderacademy.edu.au',
            to_emails=f'{order.user.email}',
            subject=f'Your order #{order.id} has been updated',
            html_content=f'''Hi, {order.user.name},<br></br><br></br>Thanks for your order!
            Your order is currently {order.status} and we will update you when this changes.
            <br></br><br></br>{order_details}Total:<br></br>${order.total_price}<br></br><br></br>
            From the Pizzeria Team!''')
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as err:
            print(str(err))

        return OrderSchema().dump(order), 201
    else:
        return {'error': f'Order not found with id {id}'}, 404

# Updates the status of an order
@order_bp.route('/status/<int:id>/', methods=['PATCH'])
@jwt_required()
def update_order_status(id):
    check_admin()
    # Loads the Schema to ensure the data is valid
    data = OrderSchema().load(request.json)
    stmt = db.select(Order).filter_by(id=id)
    order = db.session.scalar(stmt)
    if order:
        order.status = request.json['status']
        db.session.commit()

        # Loops through the order items and generates a string with all of the order details to be added to the email
        order_details = '''Order:<br></br>'''
        for order_item in order.order_items:
            order_loop = f'{order_item.quantity} * {order_item.food.name} (${order_item.food.price})<br></br>Subtotal: ${order_item.subtotal}<br></br><br></br>'
            order_details += order_loop

        # Sends an email to the user with the updated details of their order
        message = Mail(
            from_email='12849@coderacademy.edu.au',
            to_emails=f'{order.user.email}',
            subject=f'Your order #{order.id} has been updated',
            html_content=f'''Hi, {order.user.name},<br></br><br></br>Thanks for your order!
            Your order is now {order.status}.<br></br><br></br>{order_details}Total:<br></br>${order.total_price}<br></br><br></br>
            From the Pizzeria Team!''')
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as err:
            print(str(err))

        return OrderSchema().dump(order)
    else:
        return {'error': f'Order not found with id {id}'}, 404

# Deletes an order
@order_bp.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_order(id):
    check_admin()
    stmt = db.select(Order).filter_by(id=id)
    order = db.session.scalar(stmt)
    if order:
        db.session.delete(order)
        db.session.commit()
        return {'message': f'Order {id} deleted'}
    else:
        return {'error': f'Order not found with id {id}'}, 404

# Deletes an order item
@order_bp.route('/<int:id>/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_order_item(id, item_id):
    check_owner()
    stmt = db.select(OrderItem).filter_by(id=item_id)
    order_item = db.session.scalar(stmt)
    if order_item:
        db.session.delete(order_item)
        db.session.commit()
        return {'message': f'Order item {item_id} deleted from order {id}'}
    else:
        return {'error': f'Order item {item_id} not found in order {id}'}, 404
