from flask import Blueprint, request
from init import db, bcrypt
from models.food import Food, FoodSchema
from controllers.auth_controller import check_admin
from flask_jwt_extended import jwt_required

food_bp = Blueprint('food', __name__, url_prefix='/food')

# Get the list of all the food items where on_menu = True
@food_bp.route('/', methods=['GET'])
def get_menu():
    stmt = db.select(Food).filter_by(on_menu=True)
    foods = db.session.scalars(stmt)
    return FoodSchema(many=True, exclude=['on_menu']).dump(foods)

# Update food items
@food_bp.route('/<int:food_id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_food(food_id):
    check_admin()
    stmt = db.select(Food).filter_by(id=food_id)
    food = db.session.scalar(stmt)
    if food:
        food.name = request.json.get('name') or food.name
        food.price = request.json.get('price') or food.price
        food.ingredients = request.json.get('ingredients') or food.ingredients
        if request.json.get('is_veg') is not None:
            food.is_veg = request.json.get('is_veg')
        else:
            food.is_veg = food.is_veg
        if request.json.get('on_menu') is not None:
            food.on_menu = request.json.get('on_menu')
        else:
            food.on_menu = food.on_menu
        db.session.commit()
        return FoodSchema().dump(food)
    else:
        return {'error': 'Food item not found'}, 404

# Add food items
@food_bp.route('/', methods=['POST'])
@jwt_required()
def add_food():
    check_admin()
    food = Food(
        name = request.json['name'],
        price = request.json['price'],
        ingredients = request.json['ingredients'],
        is_veg = request.json['is_veg']
    )
    db.session.add(food)
    db.session.commit()
    return FoodSchema().dump(food), 201
