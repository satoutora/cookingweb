import os
from flask import Blueprint, render_template, request, flash, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from .models import User, Food, Category_food, Comments
from . import db
from flask_login import login_user, login_required, logout_user, current_user

from . import create_app

auth = Blueprint('auth', __name__)
app = create_app()

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist', category='error')        
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        city = request.form.get('city')
        avatar = request.files['avatar']
        if allowed_image(avatar.filename):
            filename = secure_filename(avatar.filename)
            avatar.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            print("Image saved")

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(email) == 0:
            flash('You must enter email', category='error')
        elif len(name) == 0:
            flash('You must enter name', category='error')
        elif password1 != password2:
            flash('Your password don' "'" 't match', category='error')
        else:
            new_user = User(email=email, 
                            name=name, 
                            password=generate_password_hash(password1, method='sha256'),
                            city=city,
                            avatar=secure_filename(avatar.filename))
            db.session.add(new_user)
            db.session.commit()
            #login_user(user, remember=True)
            flash('Your account created', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user) 

@auth.route('/add-new-recipe', methods=['GET', 'POST'])
def add_new_recipe():
    if request.method == 'POST':
        name = request.form.get('name')
        id_categoryfood = request.form.get('id_categoryfood')
        material = request.form.get('material')
        recipe = request.form.get('recipe')

        image = request.files['image']
        if allowed_image(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            print("Image saved")

        user=current_user        
        new_food = Food(name=name, 
                        id_user=user.id,
                        id_categoryfood=id_categoryfood,
                        material=material,
                        recipe=recipe,
                        image=secure_filename(image.filename))
        db.session.add(new_food)
        db.session.commit()
        #login_user(user, remember=True)
        flash('Created recipe', category='success')
        return redirect(url_for('views.userRecipe'))

    return render_template("add_new_recipe.html", user=current_user) 

@auth.route('/search', methods=['POST', 'GET'])
def search():
    foods = Food.query.all()
    if request.method == 'POST':
        ct = request.form.get('search')
        search = "%{}%".format(ct)
        print(search)
        foods = Food.query.filter(Food.name.like(search)).all()
        print(foods)
    return render_template("home.html", user=current_user, 
                                        list_user=User.query.all(), 
                                        list_food=foods,
                                        list_category=Category_food.query.all(),
                                        list_comments=Comments().query.all())
    