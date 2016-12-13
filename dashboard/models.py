from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(54))

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


class Advert(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    checksum = db.Column(db.String(256))
    date_creation = db.Column(db.DateTime(100))
    url = db.Column(db.String(250))
    website = db.Column(db.String(100))
    file_type = db.Column(db.String(50))
    original_url = db.Column(db.String(500))
    authorized = db.Column(db.String(50))
    description = db.Column(db.String(500))
    rate = db.Column(db.Integer)
    value = db.Column(db.Float, onupdate=rate/30)
    banner_size = db.Column(db.String(50))
    product = db.Column(db.String(100))
    class_customer = db.Column(db.String(100))
    category = db.Column(db.String(100))
    sector = db.Column(db.String(100))
    image_id = db.Column(db.String(100))
    

class Adtracking(db.Model):
    __tablename__ = 'adtracking'
    id = db.Column(db.Integer, primary_key=True)
    checksum = db.Column(db.String(256))
    date_creation = db.Column(db.DateTime(100))
    location = db.Column(db.String(256))


class Website(db.Model):
    __tablename__ = 'websites'
    id = db.Column(db.Integer, primary_key=True)
    domain_name = db.Column(db.String(256))
    cost = db.Column(db.Float)

    def __init__(self, domain_name, cost=0):
        self.domain_name = domain_name.lower()
        self.cost = cost
