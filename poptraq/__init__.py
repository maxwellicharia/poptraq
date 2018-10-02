from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, Manager, MigrateCommand
from flask_bootstrap import Bootstrap
from flask_debug import Debug

app = Flask(__name__)

app.config['SECRET_KEY'] = "$poptraq#"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/potraq"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

Bootstrap(app)

Debug(app)

db = SQLAlchemy(app)

from poptraq.models import User, County
from poptraq import views
from poptraq.user import views

manager = Manager(app)
manager.add_command('db', MigrateCommand)

migrate = Migrate(app, db)
