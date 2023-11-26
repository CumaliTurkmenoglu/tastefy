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


def insert(username, password,type):
    from datetime import datetime
    try:
        modelUsers = User()
        modelUsers.username = username
        modelUsers.password = password
        modelUsers.type = type
        modelUsers.date = datetime.today().date()
        db.session.add(modelUsers)
        db.session.commit()
        auto_incremented_id = modelUsers.id
        return auto_incremented_id
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False


def update_user(user_name, name=None, surname=None, age=None, gender=None, height=None, weight=None):
    try:
        user = getUserByUserName(user_name)
        if user:
            if name is not None:
                user.name = name
            if surname is not None:
                user.surname = surname
            if age is not None:
                user.age = age
            if gender is not None:
                user.gender = gender
            if height is not None:
                user.height = height
            if weight is not None:
                user.weight = weight
            db.session.commit()
            return True
        else:
            print(f"User with username {user_name} not found.")
            return False
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False


def getUserById(id):
    try:
        db.metadata.clear()
        user = User.query.filter(User.id == id).one_or_none()
        return user
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False


def getUserByUserName(userName):
    try:
        db.metadata.clear()
        return User.query.filter(User.username == userName).one_or_none()
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False


from  werkzeug.security import check_password_hash
def check_login(userName,password):
    try:
        db.metadata.clear()
        return check_password_hash(getUserByUserName(userName).password , password)
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False


def getRoleByUserName(userName):
    try:
        db.metadata.clear()
        return User.query.filter(User.username ==userName).one_or_none().type
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False


def updateRole(user,type):
    db.metadata.clear()
    try:
        user.type = type
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False


def getUserNameById(id):
    try:
        db.metadata.clear()
        name = User.query.filter(User.id == id).one_or_none().name
        return name
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False


def getUserIdByUserName(userName):
    try:
        db.metadata.clear()
        id = User.query.filter(User.username == userName).one_or_none().id
        return id
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False

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

