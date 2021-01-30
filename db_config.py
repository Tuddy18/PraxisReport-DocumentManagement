# from app import app
from flask_mysqldb import MySQL
import os
config = {}

config['MYSQL_HOST'] = 'ubb-praxis-document.cuhfzpml419o.eu-west-1.rds.amazonaws.com'
config['MYSQL_PORT'] = '3306'
config['MYSQL_USER'] = 'admin'
config['MYSQL_PASSWORD'] = 'Fw5HqelvBL2xZEjX#5JE'
config['MYSQL_DB'] = 'ubb_praxis_document'
config['MYSQL_CURSORCLASS'] = 'DictCursor'