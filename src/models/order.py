from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import OneOf
from marshmallow.exceptions import ValidationError
from sqlalchemy.ext.hybrid import hybrid_property

VALID_STATUSES = ('Pending', 'In progress', 'Ready for pick-up', 'Completed', 'Refunded')

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime)
    status = db.Column(db.String, default=VALID_STATUSES[0])
    # total_price = db.Column(db.Float)
    user = db.relationship('User', back_populates='orders')
    order_items = db.relationship('OrderItem', back_populates='order', cascade='all, delete')
    
    # Calculates the total price of the order by multiplying the quantity of each order item by each item's price
    @hybrid_property
    def total_price(self):
        total = 0
        for order_item in self.order_items:
            total += order_item.subtotal
        return total

class OrderSchema(ma.Schema):
    status = fields.String(load_default=VALID_STATUSES[0], validate=OneOf(VALID_STATUSES))
    order_items = fields.List(fields.Nested('OrderItemSchema', only=('id', 'quantity', 'subtotal', 'food')))

    @validates('status')
    def validate_status(self, value):
        if value not in VALID_STATUSES:
            raise ValidationError('Invalid status')
            
    class Meta:
        fields = ('id', 'user_id', 'date', 'status', 'total_price', 'order_items')
        ordered = True
        