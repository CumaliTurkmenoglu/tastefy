# manage.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dbenv import SSH_USERNAME,SSH_PASSWORD,DB_NAME,DB_PASSWORD,HOST,PORT,REMOTE_BIND_ADRESS
import sshtunnel
tunnel = sshtunnel.SSHTunnelForwarder(('ssh.pythonanywhere.com'),
                                      ssh_username=SSH_USERNAME,
                                      ssh_password=SSH_PASSWORD,
                                      remote_bind_address=(REMOTE_BIND_ADRESS,PORT)
                                      )
tunnel.start()
app = Flask(__name__)
app.config['SECRET_KEY'] = "KFAŞLKDJAFIDSFcnzndklsfjsdfjs"
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{SSH_USERNAME}:{DB_PASSWORD}@{HOST}:{tunnel.local_bind_port}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Set to False to suppress warning
db = SQLAlchemy(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
