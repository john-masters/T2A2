from init import db, ma

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(50))
    password = db.Column(db.String(50))
    is_admin = db.Column(db.Boolean)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'phone', 'password', 'is_admin')
        ordered = True
        