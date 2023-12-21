from flask import Flask
from flask_bootstrap import Bootstrap

from .models import db

bootstrap = Bootstrap()
app = Flask(__name__)
db.init_app(app)
bootstrap.init_app(app)
