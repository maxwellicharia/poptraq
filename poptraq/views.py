import os
import markdown
from flask import render_template, request, url_for, send_from_directory, Markup
from poptraq.form import Signup, Login
from poptraq.models import User
from poptraq import app, db, migrate


@app.route('/', methods=['GET', 'POST'])
def dash():
    return render_template('dash.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login(request.form)  # instantiating form to use the forms defined from the Form class in form.py

    if request.method == 'GET':
        return render_template('login.html', form=form)
    else:
        if not form.validate_on_submit():  # making sure that the form is validated before submission
            return render_template('login.html', form=form, not_validate=True)
        else:
            # User.__init__(national_id=request.form['national_id'],
            #               email=request.form['email'],
            #               password=request.form['password'])
            return url_for('account')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return "To configure"


@app.route('/signup', methods=['GET', 'POST'])
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


@app.route('/account/', methods=['GET', 'POST'])
def account():
    return render_template('account.html')


@app.route('/about')
def about():
    with open("./docs/README.md") as f:
        content = f.read()
    content = Markup(markdown.markdown(content))
    return render_template('about.html', **locals())


@app.route('/favicon.ico')
def fav():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


def create_app():
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    return app
