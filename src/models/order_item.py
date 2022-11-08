from init import db, ma
from marshmallow import fields

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    food = db.relationship('Food', back_populates='order_items')

class OrderItemSchema(ma.Schema):
    food = fields.Nested('FoodSchema', only=('name', 'price'))
    class Meta:
        fields = ('id', 'food_id', 'order_id', 'quantity')
        ordered = True
        