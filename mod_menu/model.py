from app import db

class Menus(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    experiment = db.Column(db.TEXT)
    foodNumber = db.Column(db.Integer)
    userId = db.Column(db.Integer)
    foodIds = db.Column(db.TEXT)
    foodNames  = db.Column(db.TEXT)
    objectives = db.Column(db.TEXT)
    violated = db.Column(db.Integer)
    nutrients = db.Column(db.TEXT)


def getUnlabelledMenusByUserId( userId):
    try:
        db.metadata.clear()
        from sqlalchemy import and_,func
        from mod_chosen_menu.model import getChosenMenusIdsByUserId,ChosenMenu
        #menus = Menus.query.join(ChosenMenu,ChosenMenu.menuId != Menus.id).filter(Menus.userId==userId).all()
        menus= (Menus.query
                .outerjoin(ChosenMenu, ChosenMenu.menuId == Menus.id).filter(ChosenMenu.menuId.is_(None))
                .filter(Menus.userId == userId)
                .all())
        #Menus.query.filter(and_(Menus.userId == userId, ~Menus.id.in_(getChosenMenuIdsByUserId(userId)))).all()
        if menus:
            return menus
        else:
            return ""
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False


def getRandomMenuByUserId(userId):
    try:
        import random
        tries = 0
        toss = random.randint(1, 2)
        experiment = 'UserCaseStudyExperiment_NSGAII_Diet_Problem_' + userId
        if toss == 2:
            experiment = 'UserCaseStudyExperiment_NSGAII_Diet_Problem_dummy' + userId
        menu = getMenuByUserId(experiment,userId)
        return menu
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False


def getMenuByUserId(experiment, userId):
    try:
        db.metadata.clear()
        from sqlalchemy import and_
        from mod_chosen_menu.model import getChosenMenuIdsByUserId
        menus = Menus.query.filter(and_(Menus.userId == userId, Menus.experiment == experiment, ~Menus.id.in_(getChosenMenuIdsByUserId(userId)))).first()
        if menus:
            return menus
        else:
            return ""
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False


def getMenuById(id):
    try:
        db.metadata.clear()
        foods = Menus.query.filter(Menus.id == id).first()
        return foods
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False


def getFoodNamesByMenuId(menuId):
    try:
        db.metadata.clear()
        menus = Menus.query.filter(Menus.id == menuId).all()
        return menus
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False

def extractObjectives(obj : str):
    import re
    import json
    objectives = []
    # Use a regular expression to find key-value pairs in the input string
    matches = re.findall(r'(\w+): ([\d.-]+)', obj)
    for match in matches:
        key, value = match
        objectives.append({"name": key, "value": float(value)})

    return objectives


def extractFoodNamesAndObjValues(menu):
    import json
    from mod_foods.model import get_food_by_id, get_food_by_ids
    food_ids = [int(id) for id in menu.foodIds.strip("'").split(',')]
    foods_with_links= get_food_by_ids(food_ids)
    food_items = menu.foodNames.rstrip(', ').split(', ')
    breakfast = []
    lunchdinner = []
    for i, food_item in enumerate(food_items):
        parts = food_item.split()
        cost = float(parts[-1])
        prep_time = float(parts[-2])
        preference = float(parts[-3])
        food_name = ' '.join(map(str, parts[:-3]))
        objectives = {
            "Cost": cost,
            "Preference": preference,
            "PreparationTime": prep_time
        }
        food = {
            "foodId": food_ids[i],
            "foodName": food_name,
            "link":foods_with_links[i].picUrl,
            "objectives": objectives
        }
        if foods_with_links[i].foodGroupId in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]:
            breakfast.append(food)
        else:
            lunchdinner.append(food)
    return breakfast, lunchdinner

def extractNutrientValues(menu):
    nutrients = {}
    parts = menu.nutrients.split("*\n")[:-1]
    for part in parts:
        lines = part.strip().split('\n')
        nutrient_name = lines[0].strip().split(',')[0]
        nutrient_data = {}
        import re
        import json
        match = re.match(r'.*#.* (\w+) :>>>>> (\d+\.\d+) LL: (\d+\.\d+) ---  UL: (\d+\.\d+) >>>> Violation: (-?\d+\.\d+)', lines[3])
        if match:
            status, amount, ll, ul, violation = match.groups()
            nutrient_data = {
                "Status": status,
                "Amount": float(amount),
                "Lower Limit": float(ll),
                "Upper Limit": float(ul),
                "Violation": float(violation)
            }
        nutrients[nutrient_name] = nutrient_data

    return nutrients


