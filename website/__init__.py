from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created database')
    # init(app)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Vjp pro'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.app_context().push()
    db.init_app(app)
    app.config["IMAGE_UPLOADS"] = "website/static/img/uploads/"
    app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
    app.config['WHOOSH_BASE'] = 'whoosh'

    #with app.app_context():
        #db.create_all()

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models import User
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app


# def init(app):
#     from .models import Category_food
#     with app.app_context():
#         cat = Category_food(name = "Món mặn")
#         db.session.add(cat)
#         cat = Category_food(name = "Món chay")
#         db.session.add(cat)
#         cat = Category_food(name = "Món canh, súp")
#         db.session.add(cat)
#         db.session.commit()

    