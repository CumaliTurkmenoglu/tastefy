from app import db
class ChosenMenu(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer)
    menuId = db.Column(db.Integer)
    feedback = db.Column(db.Integer)

def getChosenMenuIdsByUserId(id):
    db.metadata.clear()
    menu = db.session.query(ChosenMenu.menuId,ChosenMenu.userId).filter(ChosenMenu.userId == id).all()
    #db.session.query(ChosenMenu.menuId,ChosenMenu.userId).all()[0]
    return menu

def getChosenMenuById(menuId):
    db.metadata.clear()
    menus = ChosenMenu.query.filter(ChosenMenu.menuId == menuId).first()
    return menus