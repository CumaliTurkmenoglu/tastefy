from app import db

class UserFoods(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer)
    userName = db.Column(db.TEXT)
    foodId = db.Column(db.Integer)
    foodName = db.Column(db.TEXT)
    preference  = db.Column(db.Float)

def getUnlabelledFoodsByUserId(userId):
    db.metadata.clear()
    foods = UserFoods.query.filter(UserFoods.userId == userId).filter(UserFoods.preference.is_(None)).all()
    return foods

def getFoodsByUserId(userId):
    db.metadata.clear()
    foods = UserFoods.query.filter(UserFoods.userId == userId).all()
    return foods

def getFoodPreference(userId,foodId, preference):
    db.metadata.clear()
    foods = UserFoods.query.filter(UserFoods.userId == userId).all()
    return foods



def setFoodPreference(userId, foodId, preference):
    try:
        uf = UserFoods()
        uf.userId       = userId
        uf.foodId       = foodId
        uf.preference       = preference

        db.session.add(uf)
        db.session.commit()
        return True
    except:
        return False



