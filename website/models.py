from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    city = db.Column(db.String(150))
    avatar = db.Column(db.String(150))

class Food(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer)
    id_categoryfood = db.Column(db.Integer)
    name = db.Column(db.String(500))
    material = db.Column(db.String(1500))
    recipe = db.Column(db.String(50000))
    image = db.Column(db.String(200))


class Category_food(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))

class Comments(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer)
    id_categoryfood = db.Column(db.Integer)
    content = db.Column(db.String(150))

    


    