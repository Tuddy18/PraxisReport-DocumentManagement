from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db_config import config
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_selfdoc import Autodoc

PROFILE_SERVICE_URL = 'https://praxisreport-profilemanagement.azurewebsites.net/'

app = Flask(__name__)
auto = Autodoc(app)

app.config['MAIL_SERVER']='smtp.mailgun.org'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'postmaster@sandbox8a1be072fa3740108e4a3bc8563fe9cb.mailgun.org'
app.config['MAIL_PASSWORD'] = 'cbd01a420c320e3b7b9170b72f4abe54-77751bfc-4631bf20'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
mailapp = Mail(app)

CORS(app, resources={r"/*": {"origins": "*"}})
db_url = 'mysql://' + config['MYSQL_USER'] + ':' + config['MYSQL_PASSWORD'] + '@' + config['MYSQL_HOST'] + '/' + config['MYSQL_DB']
app.config['SQLALCHEMY_DATABASE_URI'] = db_url

db = SQLAlchemy(app)

from app.domain import *
from app.service import *


# db.drop_all()
db.create_all()

jwt = JWTManager(app)
