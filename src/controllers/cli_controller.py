from flask import Blueprint
from init import db, bcrypt
from datetime import date
from models.food import Food
from models.order_item import OrderItem
from models.order import Order
from models.user import User

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print('Database created!')

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print('Database dropped!')

@db_commands.cli.command('seed')
def seed_db():
    # seed the database
    users = [
        User(
            name = 'admin',
            email = '12849@coderacademy.edu.au',
            phone = '0413515596',
            password = bcrypt.generate_password_hash('password123').decode('utf-8'),
            is_admin = True
        ),
        User(
            name = 'guest',
            email = 'spam@eggs.com',
            phone = '0400000000',
            password = bcrypt.generate_password_hash('password').decode('utf-8'),
            is_admin = False
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
            ingredients = 'Mozarella, gorgonzola',
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
            status = 'pending',
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
    