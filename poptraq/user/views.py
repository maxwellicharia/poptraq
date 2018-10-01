from flask import render_template, request, session, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from poptraq.form import Signup, Login
from poptraq.models import User
from poptraq import app, db

user = Blueprint('user', __name__, url_prefix='/user', static_folder='static', template_folder='templates')


@user.route('/signup', methods=['GET', 'POST'])
def signup():
    form = Signup(request.form)

    if request.method == 'GET':
        if session.get('email') is None:
            return render_template('signup.html', form=form)
        else:
            email = session['email']
            return render_template('signup.html', form=form, email=email)
    else:
        if session.get('email') is None:
            if not form.validate_on_submit():  # making sure that the form is validated before submission
                return render_template('signup.html', form=form)
            else:
                national_id = int(request.form['national_id'])
                email = request.form['email']
                exists_id = db.session.query(User.national_id).filter_by(national_id=national_id).scalar()
                exists_email = db.session.query(User.email).filter_by(email=email).scalar()
                if (exists_id is None) and (exists_email is None):
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
                    message = session['email']
                    return render_template('account.html', message=message)
                else:
                    return render_template('signup.html', exists=True, form=form)
        else:
            email = session['email']
            return render_template('signup.html', form=form, email=email)


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = Login(request.form)  # instantiating form to use the forms defined from the Form class in form.py

    if request.method == 'GET':
        if session.get('email') is None:
            return render_template('login.html', form=form)
        else:
            email = session['email']
            return render_template('login.html', form=form, login=email)
    else:
        if not form.validate_on_submit():  # making sure that the form is validated before submission
            return render_template('login.html', form=form)
        else:
            if session.get('email') is None:
                national_id = int(request.form['national_id'])
                email = request.form['email']
                password = request.form['password']
                exists_id = db.session.query(User.national_id).filter_by(national_id=national_id).scalar()
                exists_email = db.session.query(User.email).filter_by(email=email).scalar()
                exists_password = db.session.query(User.password).filter_by(national_id=national_id,
                                                                            email=email).scalar()
                if (exists_id is not None) and (exists_email is not None) and (
                        check_password_hash(exists_password, password) is True):
                    session['email'] = exists_email
                    message = session['email']
                    return render_template('account.html', message=message)
                else:
                    if (exists_id is not None) and (exists_email is not None) and (
                            check_password_hash(exists_password, password) is False):
                        return render_template('login.html', invalid=True)
                    else:
                        return render_template('login.html', form=form, not_found=True)
            else:
                email = session['email']
                return render_template('login.html', form=form, login=email)


@user.route('/logout', methods=['GET'])
def logout():
    if session.get('email') is None:
        return render_template('index.html', log_out=True)
    else:
        session.pop('email', None)
        return render_template('index.html', success=True)


@user.route('/account', methods=['GET', 'POST'])
def account():
    if session.get('email') is None:
        return render_template('index.html', log_out=True)
    else:
        email = session['email']
        return render_template('account.html', email=email, logged_in=True)


app.register_blueprint(user)
