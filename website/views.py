from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User, Food, Category_food, Comments
from sqlalchemy import desc

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user, 
                                        list_user=User.query.all(), 
                                        list_food=Food.query.order_by(desc(Food.id)).all(),
                                        list_category=Category_food.query.all(),
                                        list_comments=Comments().query.order_by(desc(Comments.id)).all())

@views.route('/userPage')
def userPage():
    return render_template("user.html", user=current_user) 

@views.route('/userRecipe')
def userRecipe():
    return render_template("user_recipe.html", user=current_user, list_food=Food.query.order_by(desc(Food.id)).all()) 

@views.route('/detail_recipe/<int:id_food>', methods=['POST', 'GET'])
def detail_recipe(id_food):
    food = Food.query.get_or_404(id_food)
    user=current_user
    if request.method == 'POST':
        content = request.form.get('comment')
        new_cmt = Comments(id_user=user.id, id_categoryfood=food.id, content=content)
        db.session.add(new_cmt)
        db.session.commit()
        return redirect(request.url)

    return render_template("detail_recipe.html", user=current_user, 
                                                food=food,
                                                list_user=User.query.all(), 
                                                list_food=Food.query.all(),
                                                list_category=Category_food.query.all(),
                                                list_comments=Comments().query.filter_by(id_categoryfood=food.id).order_by(desc(Comments.id)).all())

@views.route('/view_user/<int:id_user>', methods=['POST', 'GET'])
def view_user(id_user):
    user = User.query.get_or_404(id_user)
    return render_template("user.html", user=user)

@views.route('/categoryFood/<int:id_category>')
def categoryFood(id_category):
    choosen_category = Category_food.query.get_or_404(id_category)
    return render_template("categoryFood.html", user=current_user,
                                                choosen_category=choosen_category,
                                                list_food=Food.query.filter_by(id_categoryfood=id_category).order_by(desc(Food.id)).all())

@views.route('/deleteRecipe/<int:id_food>', methods=['POST', 'GET'])
def deleteRecipe(id_food):
    food = Food.query.get_or_404(id_food)
    db.session.delete(food)
    db.session.commit()
    flash('Delete recipe', category='success')
    return redirect(url_for('views.userRecipe'))

