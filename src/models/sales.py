from init import db, ma

class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    total_sales = db.Column(db.Float)

class SalesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'order_id', 'total_sales')
        ordered = True
        