from app import db
class ChosenMenu(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer)
    menuId = db.Column(db.Integer)
    feedback = db.Column(db.Integer)

def getChosenMenusIdsByUserId(id):
    try:
        db.metadata.clear()
        menu = db.session.query(ChosenMenu.menuId,ChosenMenu.userId).filter(ChosenMenu.userId == id).all()
        #db.session.query(ChosenMenu.menuId,ChosenMenu.userId).all()[0]
        return menu
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False


def getChosenMenuById(menuId):
    try:
        db.metadata.clear()
        menus = ChosenMenu.query.filter(ChosenMenu.menuId == menuId).first()
        return menus
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False

def set_menu_preference(userId, menuId, preference):
    try:
        user_menu = get_user_menus_by_user_id_and_menu_id(userId, menuId)
        if user_menu:
            user_menu.userId = userId
            user_menu.foodId = menuId
            user_menu.preference = preference
            db.session.commit()
            return True
        else:
            user_menu=ChosenMenu()
            user_menu.userId = userId
            user_menu.menuId = menuId
            user_menu.feedback = preference
            db.session.add(user_menu)
            db.session.commit()
            return True
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False

def get_user_menus_by_user_id_and_menu_id(userId,menuId):
    try:
        db.metadata.clear()
        menus = ChosenMenu.query.filter(ChosenMenu.userId==userId,ChosenMenu.menuId == menuId).one_or_none()
        return menus
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False

def reset_menu_preference(userId, menuId):
    try:
        user_menu = get_user_menus_by_user_id_and_menu_id(userId, menuId)
        if user_menu:
            user_menu.userId = userId
            user_menu.foodId = menuId
            db.session.delete(user_menu)
            db.session.commit()
            return True
        else:
            return False
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False