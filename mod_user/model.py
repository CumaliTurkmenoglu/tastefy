from app import db

class User(db.Model):
    id   = db.Column(db.Integer,primary_key = True,autoincrement=True)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    type = db.Column(db.Integer)
    date = db.Column(db.DATE)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(255))
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)

#    Verify = db.Column(db.Integer)


def insert(name,surname,username, password,type,date,age,gender,height,weight):#,verify):
    try:
        modelUsers = User()
        # modelUserCompany=UserCompany()
        modelUsers.name = name
        modelUsers.surname = surname
        modelUsers.username = username
        modelUsers.password = password
        modelUsers.type = type
        modelUsers.date = date
        modelUsers.age = age
        modelUsers.gender = gender
        modelUsers.height = height
        modelUsers.weight = weight
#        modelUsers.verify = verify

        db.session.add(modelUsers)
        db.session.commit()
        return True
    except: return False

def getUserById(id):
    db.metadata.clear()
    user = User.query.filter(User.id == id).one_or_none()
    return user

def getUserByUserName(userName):
    db.metadata.clear()
    return User.query.filter(User.username == userName).one_or_none()

from  werkzeug.security import check_password_hash
def check_login(userName,password):
    db.metadata.clear()
    return check_password_hash(getUserByUserName(userName).password , password)

def getRoleByUserName(userName):
    db.metadata.clear()
    return User.query.filter(User.username ==userName).one_or_none().type

def updateRole(user,type):
    db.metadata.clear()
    try:
        user.type = type
        db.session.commit()
        return True
    except: return False

def getUserNameById(id):
    db.metadata.clear()
    name = User.query.filter(User.id == id).one_or_none().name
    return name

def getUserIdByUserName(userName):
    db.metadata.clear()
    id = User.query.filter(User.username == userName).one_or_none().id
    return id

#
# def check_verify(email):
#     db.metadata.clear()
#     model = User.query.filter(User.Email == email).one_or_none().Verify
#     return model
#
# def updateVerify(email):
#     db.metadata.clear()
#     try:
#         admin = User.query.filter(User.Email == email, User.Verify == 0).first()
#         admin.Verify = 1
#         db.session.commit()
#         return True
#     except: return False

