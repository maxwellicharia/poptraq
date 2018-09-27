from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, Manager, MigrateCommand
from form import Signup
from models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = "$poptraq#"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost/poptraq"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
migrate = Migrate(app, db)
Bootstrap(app)


@app.route('/')
def dash():
    return render_template("dash.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/logout')
def logout():
    return "To configure"


@app.route('/signup')
def signup():
    form = Signup(request.form)  # instantiating form to use the forms defined from the Form class in form.py

    if request.method == 'GET':
        return render_template('signup.html', form=form)
    else:
        if not form.validate_on_submit():  # making sure that the form is validated before submission
            return render_template('signup.html', form=form, not_validate=True)
        else:
            User.__init__(national_id=request.form['national_id'],
                          first_name=request.form['first_name'],
                          surname=request.form['surname'],
                          dob=request.form['dob'],
                          home_county=request.form['home_county'],
                          email=request.form['email'],
                          password=request.form['password'])
            return url_for('account')


@app.route('/account/')
def account():
    return render_template("account.html")
