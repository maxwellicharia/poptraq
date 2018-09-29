from flask import render_template, request, url_for, session, redirect, Blueprint, abort
from werkzeug.security import generate_password_hash, check_password_hash
from poptraq.form import Signup, Login
from poptraq.models import User
from poptraq import app, db

user = Blueprint('user', __name__, url_prefix='/user', static_folder='static', template_folder='templates')


@user.route('/signup', methods=['GET', 'POST'])
def signup():
    form = Signup(request.form)  # instantiating form to use the forms defined from the Form class in form.py

    if request.method == 'GET':
        return render_template('signup.html', form=form)
    else:
        if not form.validate_on_submit():  # making sure that the form is validated before submission
            return render_template('signup.html', form=form)
        else:
            pw_hash = generate_password_hash(request.form['password'], method='pbkdf2:sha256', salt_length=8)
            new_user = User(request.form['national_id'],
                            request.form['first_name'],
                            request.form['surname'],
                            request.form['dob'],
                            request.form['home_county'],
                            request.form['email'],
                            pw_hash)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = request.form['email']
            return redirect(url_for('user.account'))


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = Login(request.form)  # instantiating form to use the forms defined from the Form class in form.py

    if request.method == 'GET':
        return render_template('login.html', form=form)
    else:
        if not form.validate_on_submit():  # making sure that the form is validated before submission
            return render_template('login.html', form=form)
        else:
            national_id = request.form['national_id']
            email = request.form['email'],
            password = request.form['password']
            exists = User.query.filter_by(national_id=national_id).first_or_404()
            if (email != exists.email) and (check_password_hash(exists.password, password) is False):
                abort(401)
            else:
                session['email'] = email
                message = ("Successful login: ", email[0])
                return render_template('account.html', message=message)


@user.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


@user.route('/account', methods=['GET', 'POST'])
def account():
    return render_template('account.html')


app.register_blueprint(user)
