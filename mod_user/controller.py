import time

from flask import Blueprint,render_template,abort,request,jsonify,flash
mod_user = Blueprint('auth',__name__)
from  werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,jwt_required,decode_token,create_refresh_token
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()


@mod_user.route('/register', methods=['POST'])
def register():
    if request.method == "POST":
        req_jeson = request.json
        username = req_jeson['username']
        password = req_jeson['password']
        type = 1
        from mod_user.model import getUserByUserName
        from mod_foods.model import get_foods_by_case_id
        if bool(getUserByUserName(username)):
            return jsonify(message="The email is already registered"), 409
        else:
            from mod_user.model import insert
            id=insert(username, generate_password_hash(password, method='SHA256'),type)
            if id:
                try:
                    from mod_user_foods.model import insert_user_foods
                    foods= get_foods_by_case_id(1)
                    insert_user_foods(id, username, foods)
                    return jsonify(message='User added succesfully'), 201
                except:
                    return "nooo"
            else:
                return abort(404)

@mod_user.route('/updateuser', methods=['POST'])
@jwt_required()
def update_user():
    if request.method == "POST":
        req_jeson = request.json
        name = req_jeson['name']
        surname = req_jeson['surname']
        age = req_jeson['age']
        gender = req_jeson['gender']
        height = req_jeson['height']
        weight = req_jeson['weight']

        current_user = protected(get_jwt_identity())
        user_id=current_user[0].json["user_id"]
        from mod_user.model import getUserByUserName
        from mod_user.model import update_user
        update=update_user(user_id, name,surname,age,gender,height,weight)
        if update:
#            refresh()
            return jsonify({"msg": "User updated succesfully", "exp": get_jwt()['exp']-time.time()}), 201
        else:
            return abort(404)

@mod_user.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        req_jeson = request.json
        username = req_jeson['username']
        password = req_jeson['password']
    if request.method == "GET":
        args=request.args
        username=args.get('username')
        password=args.get('password')

    from mod_user.model import getUserById,getUserIdByUserName,check_login,getRoleByUserName

    if bool(getUserIdByUserName(username)):
        if check_login(username,password):
            userId =  str(getUserIdByUserName(username))
            role = str(getRoleByUserName(username))
            access_token = create_access_token(identity=username+"*"+role +"*"+userId)
            refresh_token = create_refresh_token(identity=username+"*"+role +"*"+userId)
            return jsonify(message="Login Succeeded!", access_token=access_token,refresh_token=refresh_token), 200
        else:
            return jsonify({"msg": "Bad username or password"}), 401

    else:
        return jsonify(message="Bad Email or Password!"), 401


@mod_user.route("/getuser", methods=["POST"])
@jwt_required()
def get_user():
    from mod_user.model import getUserById
    current_user=protected(get_jwt_identity())
    user=getUserById(current_user[0].json["user_id"])
    return jsonify(name=user.name, surname=user.surname, age=user.age, gender=user.gender, height=user.height, weight=user.weight).json


@mod_user.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)

def protected(current_user):
    username, role, userId = current_user.split('*')
    return jsonify(username=username, user_role=role, user_id=userId), 200

#
# @mod_user.route("/verify", methods=["GET"])
# def updateVerify_email():
#     from mod_user.model import updateVerify
#     args=request.args
#     email=args.get('email')
#     success = updateVerify(email)
#     if success:
#         #flash("E-mail verification is succesful")
#         #return redirect("http://127.0.0.1:5000/login/")
#         return jsonify({'Status': 'Success'})
#     else:
#         return abort(404)
#
#     from mod_user.model import check_login,check_verify
#     from mod_user.model import get_user,getuserIdByemail,getrolebyemail
#
#     if check_verify(email) == 0:
#         return jsonify(message="Please verify your e-mail address"), 401
#     else:
#         if bool(get_user(email)):
#             if check_login(email,password):
#                 userId =  str(getuserIdByemail(email))
#                 role = str(getrolebyemail(email))
#                 access_token = create_access_token(identity=email+"*"+role +"*"+"*"+userId)
#                 refresh_token = create_refresh_token(identity=email+"*"+role +"*"+"*"+userId)
#                 return jsonify(message="Login Succeeded!", access_token=access_token,refresh_token=refresh_token), 201
#             else:
#                 return jsonify(message="Bad Email or Password"), 401
#
#         else:
#             return jsonify(message="Bad Email or Password"), 401
