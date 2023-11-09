from flask import Blueprint,render_template,redirect,url_for,abort,request,jsonify,flash
mod_user = Blueprint('auth',__name__)
from  werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required,decode_token,create_refresh_token
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()


@mod_user.route('/register', methods=['POST'])
def register():
    if request.method == "POST":
        req_jeson = request.json
        name = req_jeson['name']
        surname = req_jeson['surname']
        username = req_jeson['username']
        password = req_jeson['password']
        type = req_jeson['type']
        date = req_jeson['date']
        age = req_jeson['age']
        gender = req_jeson['gender']
        height = req_jeson['height']
        weight = req_jeson['weight']

        from mod_user.model import getUserByUserName
        if bool(getUserByUserName(username)):
            return jsonify(message="The email is already registered"), 409

        else:
            from mod_user.model import insert
            add=insert(name, surname, username, generate_password_hash(password, method='SHA256'),type,date,age,gender,height,weight)
            if add:
                return jsonify(message='User added succesfully'), 201
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
            return jsonify(message="Login Succeeded!", access_token=access_token,refresh_token=refresh_token), 201
        else:
            return jsonify(message="Bad Email or Password"), 401

    else:
        return jsonify(message="Bad Email or Password"), 401




@mod_user.route("/getuser", methods=["POST"])
@jwt_required()
def get_user():
    from mod_user.model import getUserById
    req_jeson = request.json
    id = req_jeson['id']
    return jsonify(str(getUserById(id)))


@mod_user.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)

@mod_user.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

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
