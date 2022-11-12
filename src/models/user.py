from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    orders = db.relationship('Order', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):
    orders = fields.List(fields.Nested('OrderSchema', exclude=['user']))

    class Meta:
        fields = ('id', 'name', 'email', 'password', 'is_admin', 'orders')
        ordered = True
        