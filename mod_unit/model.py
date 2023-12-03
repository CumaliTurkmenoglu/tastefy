from app import db

class Units(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.TEXT)

def get_unit_by_id(id):
    try:
        db.metadata.clear()
        foods = Units.query.filter(Units.id == id).first()
        return foods
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False

def get_nutrients_by_ids(ids):
    try:
        db.metadata.clear()
        ingredients = Units.query.filter(Units.id.in_(ids)).all()
        return ingredients
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False



