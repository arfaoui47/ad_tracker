# import os

# # Grabs the folder where the script runs.
# basedir = os.path.abspath(os.path.dirname(__file__))

# # Enable debug mode.
DEBUG = True

# # Secret key for session management. You can generate random strings here:
# # http://clsc.net/tools-old/random-string-generator.php
SECRET_KEY = 'my precious'

MYSQL_DATABASE_USER = 'root'
MYSQL_DATABASE_HOST = 'localhost'
MYSQL_DATABASE_PASSWORD = 'arfa47'
MYSQL_DATABASE_DB = 'test3'
# # Connect to the database
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')

SQLALCHEMY_DATABASE_URI = 'mysql://root:arfa47@localhost/test3'
from app import app
from models import db
