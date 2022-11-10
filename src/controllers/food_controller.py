from flask import Blueprint, request
from init import db, bcrypt
from models.food import Food, FoodSchema
from controllers.auth_controller import check_admin
from flask_jwt_extended import jwt_required

food_bp = Blueprint('food', __name__, url_prefix='/food')

# Get the list of all the food items (menu)
@food_bp.route('/', methods=['GET'])
def menu():
    stmt = db.select(Food)
    foods = db.session.scalars(stmt)
    return FoodSchema(many=True).dump(foods)

# Update food items
@food_bp.route('/<int:food_id>/', methods=['PUT'])
@jwt_required()
def update_food(food_id):
    check_admin()
    stmt = db.select(Food).filter_by(id=food_id)
    food = db.session.scalar(stmt)
    if food:
        food.name = request.json.get('name') or food.name
        food.price = request.json.get('price') or food.price
        food.ingredients = request.json.get('ingredients') or food.ingredients
        food.is_veg = request.json.get('is_veg') or food.is_veg
        db.session.commit()
        return FoodSchema().dump(food)
    else:
        return {'error': 'Food item not found'}, 404

# Delete food items
# @food_bp.route('/<int:food_id>/', methods=['DELETE'])
# @jwt_required()
# def delete_food(food_id):
#     check_admin()
#     stmt = db.select(Food).filter_by(id=food_id)
#     food = db.session.scalar(stmt)
#     if food:
#         db.session.delete(food)
#         db.session.commit()
#         return {'message': f'Food item {food.name} deleted'}
#     else:
#         return {'error': 'Food item not found'}, 404

# Add food items
