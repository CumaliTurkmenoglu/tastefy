import sshtunnel
from flask import Flask
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from dbenv import DB_NAME, DB_USERNAME,DB_PASSWORD,HOST,PORT #SSH_USERNAME,SSH_PASSWORD,REMOTE_BIND_ADRESS
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

import mysql.connector  # Import the MySQL connector library

#pythonanywhere mysql bağlantısı
# tunnel = sshtunnel.SSHTunnelForwarder(('ssh.pythonanywhere.com'),
#                                       ssh_username=SSH_USERNAME,
#                                       ssh_password=SSH_PASSWORD,
#                                       remote_bind_address=(REMOTE_BIND_ADRESS,PORT)
#                                       )
# tunnel.start()

app = Flask(__name__)
jwt = JWTManager(app)

# Configure the SQLAlchemy database URI
app.config['SECRET_KEY'] = "KFAŞLKDJAFIDSFcnzndklsfjsdfjs"
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{HOST}:{PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy database instance
db = SQLAlchemy(app)

@app.context_processor
def today():
    return {'now': datetime.now().strftime("%Y-%m-%d")}

app.config['SECRET_KEY'] = "KFAŞLKDJAFIDSFcnzndklsfjsdfjs"
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{SSH_USERNAME}:{DB_PASSWORD}@{HOST}:{tunnel.local_bind_port}/{DB_NAME}'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

from mod_user.controller import mod_user
from mod_control.controller import mod_controller
from mod_menu.controller import mod_menu
migrate = Migrate(app,db)

app.register_blueprint(mod_controller ,url_prefix='/controller')
app.register_blueprint(mod_user,url_prefix='/auth')
app.register_blueprint(mod_menu,url_prefix='/menu')

import pandas as pd

from flask import jsonify
from mod_foods.model import getFoodsByCategory
@app.route('/')
def index():
    try:
        # Start a transaction
        with db.session.begin_nested():
            foods = getFoodsByCategory(1)
            return jsonify({'Data': {'Name': foods.name}})
    except Exception as e:
        # Handle exceptions and roll back the transaction
        db.session.rollback()
        return str(e)




import os
port = int(os.environ.get("PORT", 5000))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
