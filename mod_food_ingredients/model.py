from app import db

class FoodIngredients(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    foodId=db.Column(db.Integer)
    ingredientId=db.Column(db.Integer)
    quantity = db.Column(db.Float)


def get_food_ingredient_by_food_id(id):
    try:
        db.metadata.clear()
        foods = FoodIngredients.query.filter(FoodIngredients.id == id).first()
        return foods
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False

def get_ingredients_by_food_ids(ids):
    try:
        db.metadata.clear()
        ingredients = FoodIngredients.query.filter(FoodIngredients.foodId.in_(ids)).all()
        return ingredients
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False
