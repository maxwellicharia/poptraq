from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from form import Signup

app = Flask(__name__)
app.config['SECRET_KEY'] = "$poptraq#"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost/poptraq"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
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
        return render_template('create.html', form=form)
    else:
        if not form.validate_on_submit():  # making sure that the form is validated before submission
            return render_template('create.html', form=form, not_validate=True)
        else:
            db = Models()
            db.create()
            name = request.form['note_name']
            subject = request.form['note_subject']
            content = request.form['note_content']
            db.insert(name, subject, content)
            return url_for('account', create=True)
