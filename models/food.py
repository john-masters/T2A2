from init import db, ma

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    ingredients = db.Column(db.String(200))
    price = db.Column(db.Float)
    is_veg = db.Column(db.Boolean)

class FoodSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'ingredients', 'price', 'is_veg')
        ordered = True
        