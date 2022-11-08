from init import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf

VALID_STATUSES = ('received', 'in-progress', 'ready', 'picked-up', 'cancelled', 'completed', 'refunded')

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime)
    status = db.Column(db.String, default = VALID_STATUSES[0])
    total_price = db.Column(db.Float)
    user = db.relationship('User', back_populates='orders')

class OrderSchema(ma.Schema):
    status = fields.String(load_default=VALID_STATUSES[0], validate=OneOf(VALID_STATUSES))
    class Meta:
        fields = ('id', 'user_id', 'date', 'status', 'total_price')
        ordered = True
        