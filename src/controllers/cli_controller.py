from flask import Blueprint
from init import db, bcrypt
from datetime import date
from models.food import Food
from models.order_item import OrderItem
from models.order import Order
from models.user import User

db_bp = Blueprint('db', __name__)

@db_bp.cli.command('create')
def create_db():
    db.create_all()
    print('Database created!')

@db_bp.cli.command('drop')
def drop_db():
    db.drop_all()
    print('Database dropped!')

@db_bp.cli.command('seed')
def seed_db():
    # seed the database
    users = [
        User(
            name = 'Admin User',
            email = '12849@coderacademy.edu.au',
            password = bcrypt.generate_password_hash('password123').decode('utf-8'),
            is_admin = True
        ),
        User(
            name = 'Bob Smith',
            email = 'spam@eggs.com',
            password = bcrypt.generate_password_hash('password').decode('utf-8')
        )
    ]
    db.session.add_all(users)
    db.session.commit()
    food = [
        Food(
            name = 'Margherita',
            ingredients = 'Tomato, basil, mozzarella',
            price = 10.00,
            is_veg = True
        ),
        Food(
            name = 'Pepperoni',
            ingredients = 'Tomato, basil, mozzarella, pepperoni',
            price = 12.00,
            is_veg = False
        ),
        Food(
            name = 'Gorgonzola',
            ingredients = 'Mozzarella, gorgonzola',
            price = 10.00,
            is_veg = True
        )
    ]
    db.session.add_all(food)
    db.session.commit()
    orders = [
        Order(
            user_id = 1,
            date = date.today(),
            total_price = 10.00
        )
    ]
    db.session.add_all(orders)
    db.session.commit()
    order_items = [
        OrderItem(
            food_id = 1,
            order_id = 1,
            quantity = 2
        ),
        OrderItem(
            food_id = 2,
            order_id = 1,
            quantity = 1
        )
    ]
    db.session.add_all(order_items)
    db.session.commit()
    print('Database seeded!')
    