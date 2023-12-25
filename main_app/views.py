from main_app import (
    app, db,
    login_manager,
)
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

from werkzeug.security import generate_password_hash, check_password_hash

from .models.users import User
from .forms import LoginForm, RegisterForm


login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=["GET", "POST"])
def login():
    msg = None
    if current_user.is_authenticated:
        return redirect(url_for('home'))  # Replace 'home' with the name of your home page's route

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()  # Adjust if your user model uses a different field for username
        
        if user is None:
            msg = 'No account found with that username. Please try again.'
        elif not user.check_password(form.password.data): 
            msg = 'Login Unsuccessful. Password is incorrect!!!'
        else:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))  # Replace 'home' with your home page's route name
    
    return render_template('auth/login.html', title='Login', form=form, error_message=msg)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            name=form.name.data, 
            email=form.email.data, 
            password_hash=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', title='Register', form=form)


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")