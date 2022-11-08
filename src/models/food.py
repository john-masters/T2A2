from init import db, ma
from marshmallow import fields

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    ingredients = db.Column(db.String(200))
    price = db.Column(db.Float)
    is_veg = db.Column(db.Boolean)
    order_items = db.relationship('OrderItem', back_populates='food')

class FoodSchema(ma.Schema):
    order_items = fields.Nested('OrderItemSchema')
    class Meta:
        fields = ('id', 'name', 'ingredients', 'price', 'is_veg')
        ordered = True
        