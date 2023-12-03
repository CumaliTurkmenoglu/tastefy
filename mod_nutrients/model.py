from app import db

class Nutrients(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.TEXT)
    nGroupId = db.Column(db.Integer)
    unitId = db.Column(db.Integer)

def get_nutrient_by_id(id):
    try:
        db.metadata.clear()
        foods = Nutrients.query.filter(Nutrients.id == id).first()
        return foods
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False

def get_nutrients_by_ids(ids):
    try:
        db.metadata.clear()
        ingredients = Nutrients.query.filter(Nutrients.id.in_(ids)).all()
        ingredients = sorted(Nutrients, key=lambda x: ids.index(x.id))
        return ingredients
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False



