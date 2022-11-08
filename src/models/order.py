from init import db, ma

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_item_id = db.Column(db.Integer, db.ForeignKey('order_items.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    total_price = db.Column(db.Float)

class OrderSchema(ma.Schema):
    class Meta:
        fields = ('id', 'order_item_id', 'user_id', 'date', 'status', 'total_price')
        ordered = True
        