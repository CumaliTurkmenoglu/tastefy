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

def getFoodsByCategory(groupId):
    db.metadata.clear()
    foods = Foods.query.filter(Foods.foodGroupId == groupId).all()
    return foods

def getFoodById(foodId):
    db.metadata.clear()
    food = Foods.query.filter(Foods.id == foodId).first()
    return food

def getFoodByIds(foodIds):
    db.metadata.clear()
    foods = Foods.query.filter(Foods.id.in_(foodIds)).all()
    foods = sorted(foods, key=lambda x: foodIds.index(x.id))
    return foods

def getFoodByName(foodName):
    db.metadata.clear()
    foods = Foods.query.filter(Foods.name == foodName).all()
    return foods



