from app import db


class FoodNutrients(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    foodId = db.Column(db.Integer)
    nutrientId = db.Column(db.Integer)
    quantity = db.Column(db.Float)



def get_nutrients_by_food_id(id):
    try:
        db.metadata.clear()
        nutrients = FoodNutrients.query.filter(FoodNutrients.id == id).first()
        return nutrients
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False


def get_nutrients_by_food_ids(ids):
    try:
        db.metadata.clear()
        nutrients = FoodNutrients.query.filter(FoodNutrients.foodId.in_(ids)).all()
        return nutrients
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False
