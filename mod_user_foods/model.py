from app import db

class UserFoods(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer)
    userName = db.Column(db.TEXT)
    foodId = db.Column(db.Integer)
    foodName = db.Column(db.TEXT)
    preference  = db.Column(db.Float)

def insert_user_foods(user_id, user_name, foods):
    try:
        user_foods = []
        for food in foods:
            # Create an instance of UserFood and associate it with the user
            user_food = UserFoods()
            user_food.userId= user_id
            user_food.userName=user_name
            user_food.foodId=food.id
            user_food.foodName=food.name
            user_foods.append(user_food)
        db.session.add_all(user_foods)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False


def getUnlabelledFoodsByUserId(userId):
    try:
        db.metadata.clear()
        foods = UserFoods.query.filter(UserFoods.userId == userId).filter(UserFoods.preference.is_(None)).all()
        return foods
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False


def getFoodsByUserId(userId):
    try:
        db.metadata.clear()
        foods = UserFoods.query.filter(UserFoods.userId == userId).all()
        return foods
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False

def getFoodPreference(userId,foodId, preference):
    try:
        db.metadata.clear()
        foods = UserFoods.query.filter(UserFoods.userId == userId).all()
        return foods
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False


def get_user_foods_by_user_id_and_food_id(userId, foodId):
    try:
        db.metadata.clear()
        return UserFoods.query.filter(UserFoods.userId == userId,UserFoods.foodId == foodId).one_or_none()
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False


def set_food_preference(userId, foodId, preference):
        try:
            user_food = get_user_foods_by_user_id_and_food_id(userId,foodId)
            user_food.userId= userId
            user_food.foodId= foodId
            user_food.preference= preference
#            db.session.add(uf)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return False




