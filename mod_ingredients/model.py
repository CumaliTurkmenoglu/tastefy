from app import db

class Ingredients(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.TEXT)

def get_ingredient_by_id(id):
    try:
        db.metadata.clear()
        foods = Ingredients.query.filter(Ingredients.id == id).first()
        return foods
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False

def get_ingredients_by_ids(ids):
    try:
        db.metadata.clear()
        ingredients = Ingredients.query.filter(Ingredients.id.in_(ids)).all()
        ingredients = sorted(Ingredients, key=lambda x: ids.index(x.id))
        return ingredients
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False
