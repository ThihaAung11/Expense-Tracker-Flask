from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager


app = Flask(__name__)
# Config
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///finance_tracker.db"
app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False 
app.config['SECRET_KEY'] = "flask"

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager(app)


from .models.users import User

with app.app_context():
    db.create_all()
    
from main_app import views