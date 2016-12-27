import os
from configparser import ConfigParser


path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
config = ConfigParser()
config.read(os.path.join(dir_path, '../config.ini'))

# # Enable debug mode.
DEBUG = True

# # Secret key for session management. You can generate random strings here:
# # http://clsc.net/tools-old/random-string-generator.php
SECRET_KEY = 'my precious'

MYSQL_DATABASE_USER = config.get('MySQL', 'user')
MYSQL_DATABASE_HOST = config.get('MySQL', 'host')
MYSQL_DATABASE_PASSWORD = config.get('MySQL', 'password')
MYSQL_DATABASE_DB = config.get('MySQL', 'db')

SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(config.get('MySQL', 'user'),
													   config.get('MySQL', 'password'),
													   config.get('MySQL', 'host')
													   config.get('MySQL', 'db'))
SQLALCHEMY_TRACK_MODIFICATIONS = True
WHOOSH_BASE = 'whoosh'
