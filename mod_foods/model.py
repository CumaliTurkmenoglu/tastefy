from app import db

class Foods(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.TEXT)
    foodGroupId = db.Column(db.Integer)
    caseStudy = db.Column(db.Integer)
    portion = db.Column(db.Integer)
    cost  = db.Column(db.Float)
    preference = db.Column(db.Float)
    preference2 = db.Column(db.Float)
    preparingTime = db.Column(db.Float)
    cookingTime = db.Column(db.Float)
    rating = db.Column(db.Float)
    co2 = db.Column(db.Float)
    availability = db.Column(db.Integer)
    picUrl = db.Column(db.TEXT)
    nameRoots = db.Column(db.TEXT)

def get_foods_by_category(groupId):
    db.metadata.clear()
    foods = Foods.query.filter(Foods.foodGroupId == groupId).all()
    return foods

def get_foods_by_case_id(case_id=1):
    try:
        db.metadata.clear()
        foods = Foods.query.filter(Foods.caseStudy == case_id).all()
        return foods
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False


def getFoodById(foodId):
    try:
        db.metadata.clear()
        food = Foods.query.filter(Foods.id == foodId).first()
        return food
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False


def getFoodByIds(foodIds):
    try:
        db.metadata.clear()
        foods = Foods.query.filter(Foods.id.in_(foodIds)).all()
        foods = sorted(foods, key=lambda x: foodIds.index(x.id))
        return foods
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False

def getFoodByName(foodName):
    try:
        db.metadata.clear()
        foods = Foods.query.filter(Foods.name == foodName).all()
        return foods
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False



