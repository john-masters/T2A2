from init import db, ma
from marshmallow import fields
from sqlalchemy.ext.hybrid import hybrid_property

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    order = db.relationship('Order', back_populates='order_items')
    food = db.relationship('Food', back_populates='order_items')

# Creates a column that calculates the subtotal of the order item
    @hybrid_property
    def subtotal(self):
        return self.quantity * self.food.price

class OrderItemSchema(ma.Schema):
    food = fields.Nested('FoodSchema', only=('name', 'price'))
    class Meta:
        fields = ('id', 'order_id', 'food_id', 'quantity', 'order', 'food', 'subtotal')
        ordered = True
        