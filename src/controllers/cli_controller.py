from flask import Blueprint
from init import db, bcrypt
from datetime import date
from models.food import Food
from models.order_item import OrderItem
from models.order import Order
from models.user import User

db_bp = Blueprint('db', __name__)

# Terminal command to create the database
@db_bp.cli.command('create')
def create_db():
    db.create_all()
    print('Database created!')

# Terminal command to drop the database
@db_bp.cli.command('drop')
def drop_db():
    db.drop_all()
    print('Database dropped!')

# Terminal command to seed the database with test data
@db_bp.cli.command('seed')
def seed_db():
    users = [
        User(
            name = 'Admin User',
            email = 'admin@email.com',
            password = bcrypt.generate_password_hash('password').decode('utf-8'),
            is_admin = True
        ),
        User(
            name = 'Bob Smith',
            email = 'user@email.com',
            password = bcrypt.generate_password_hash('password').decode('utf-8')
        ),
        User(
            name = 'John Smith',
            email = 'user1@email.com',
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
            price = 15.00,
            is_veg = False
        ),
        Food(
            name = 'Gorgonzola',
            ingredients = 'Mozzarella, gorgonzola',
            price = 12.00,
            is_veg = True
        )
    ]
    db.session.add_all(food)
    db.session.commit()
    orders = [
        Order(
            user_id = 2,
            date = date.today()
        ),
        Order(
            user_id = 3,
            date = date.today()
        )
    ]
    db.session.add_all(orders)
    db.session.commit()
    order_items = [
        OrderItem(
            order_id = 1,
            food_id = 1,
            quantity = 2
        ),
        OrderItem(
            order_id = 1,
            food_id = 2,
            quantity = 1
        ),
        OrderItem(
            order_id = 2,
            food_id = 3,
            quantity = 1
        ),
        OrderItem(
            order_id = 2,
            food_id = 1,
            quantity = 2
        )
    ]
    db.session.add_all(order_items)
    db.session.commit()
    print('Database seeded!')
    