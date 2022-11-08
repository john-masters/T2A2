from init import db, ma

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))

class MenuSchema(ma.Schema):
    class Meta:
        fields = ('id', 'food_id')
        ordered = True
        