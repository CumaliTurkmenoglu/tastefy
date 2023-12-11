import sshtunnel
from flask import Flask, session, request
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from dbenv import (HOST,PORT, SSH_USERNAME,SSH_PASSWORD,REMOTE_BIND_ADRESS, DB_NAME, DB_PASSWORD,
                   DB_PASSWORD_HOSTINGER, DB_NAME_HOSTINGER, PORT_HOSTINGER, DB_USERNAME_HOSTINGER, HOST_HOSTINGER)
from datetime import datetime,timedelta

#from flask_bootstrap import Bootstrap
#from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required
import mysql.connector

def connect_hostinger_db():
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{DB_USERNAME_HOSTINGER}:{DB_PASSWORD_HOSTINGER}@{HOST_HOSTINGER}:{PORT_HOSTINGER}/{DB_NAME_HOSTINGER}'
    return SQLALCHEMY_DATABASE_URI
def connect_pythonanywhere_db_from_local():
    tunnel = sshtunnel.SSHTunnelForwarder(('ssh.pythonanywhere.com'),
                                          ssh_username=SSH_USERNAME,
                                          ssh_password=SSH_PASSWORD,
                                          remote_bind_address=(REMOTE_BIND_ADRESS, PORT)
                                          )
    tunnel.start()
    SQLALCHEMY_DATABASE_URI = f'mysql://{SSH_USERNAME}:{DB_PASSWORD}@{HOST}:{tunnel.local_bind_port}/{DB_NAME}'
    return SQLALCHEMY_DATABASE_URI
def connect_pythonanywhere_db_from_pythonanywhere():
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
        username=SSH_USERNAME,
        password=DB_PASSWORD,
        hostname=REMOTE_BIND_ADRESS,
        databasename=DB_NAME)
    return SQLALCHEMY_DATABASE_URI

app = Flask(__name__)

from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

#SQLALCHEMY_DATABASE_URI = connect_hostinger_db()
SQLALCHEMY_DATABASE_URI = connect_pythonanywhere_db_from_local()
#SQLALCHEMY_DATABASE_URI = connect_pythonanywhere_db_from_pythonanywhere()  # live

app.config['SECRET_KEY'] = "KFAŞLKDJAFIDSFcnzndklsfjsdfjs"
app.config["SQLALCHEMY_DATABASE_URI"]=SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=180)  # days=30)

jwt = JWTManager(app)
db = SQLAlchemy(app)

@app.context_processor
def today():
    return {'now': datetime.now().strftime("%Y-%m-%d")}

from mod_user.controller import mod_user
from mod_control.controller import mod_controller
from mod_menu.controller import mod_menu
migrate = Migrate(app,db)

app.register_blueprint(mod_controller ,url_prefix='/controller')
app.register_blueprint(mod_user,url_prefix='/auth')
app.register_blueprint(mod_menu,url_prefix='/menu')


@app.errorhandler(401)
def unauthorized(error):
    from flask import redirect
    from flask import url_for
    return redirect(url_for('https://www.tastefy.net/login.php'))

from flask import jsonify
# from mod_foods.model import get_foods_by_category
# @app.route('/')
# def index():
#     try:
#         # Start a transaction
#         with db.session.begin_nested():
#             foods = get_foods_by_category(1)
#             return jsonify({'Data': {'Name': foods.name}})
#     except Exception as e:
#         # Handle exceptions and roll back the transaction
#         db.session.rollback()
#         return str(e)

# @app.route("/callback")
# @jwt_required()
# def callback():
#     import requests
#     ltoken =  session.get("refresh_token")
#     url = "https://cml.pythonanywhere.com/auth/refresh"
#     payload = {}
#     headers = {
#         'Authorization': 'Bearer ' + ltoken
#     }
#     response = requests.request("POST", url, headers=headers, data=payload).json()
#     return response


import os
port = int(os.environ.get("PORT", 5000))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
