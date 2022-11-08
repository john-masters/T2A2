from init import db, ma

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    quantity = db.Column(db.Integer)

class OrderItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'food_id', 'order_id', 'quantity')
        ordered = True
        