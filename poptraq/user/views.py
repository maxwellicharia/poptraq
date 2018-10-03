import datetime
import json
import requests
from flask import render_template, request, session, Blueprint, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from poptraq.email import send_email
from poptraq.form import Signup, Login
from poptraq.models import User
from poptraq import app, db
from poptraq.user.token import generate_confirmation_token, confirm_token
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
                captcha_response = request.form['g-recaptcha-response']
                if is_human(captcha_response):
                    national_id = int(request.form['national_id'])
                    email = request.form['email']
                    exists_id = db.session.query(User.national_id).filter_by(national_id=national_id).scalar()
                    exists_email = db.session.query(User.email).filter_by(email=email).scalar()
                    if (exists_id is None) and (exists_email is None):
                        pw_hash = generate_password_hash(request.form['password'], method='pbkdf2:sha256',
                                                         salt_length=8)
                        new_user = User(request.form['national_id'],
                                        request.form['first_name'],
                                        request.form['surname'],
                                        request.form['dob'],
                                        request.form['home_county'],
                                        request.form['email'],
                                        pw_hash)
                        db.session.add(new_user)
                        db.session.commit()
                        session['email'] = new_user.email
                        token = generate_confirmation_token(new_user.email)
                        confirm_url = url_for('user.confirm_email', token=token, _external=True)
                        name = new_user.first_name
                        html = render_template('activate.html', confirm_url=confirm_url, name=name)
                        subject = "Please confirm your email"
                        send_email(new_user.email, subject, html)
                        # To thread it and run in the background
                        return render_template("account.html", sent=True)
                    else:
                        return render_template('signup.html', exists=True, form=form)
                else:
                    # Log invalid attempts
                    status = "Sorry ! Bots are not allowed."
        else:
            email = session['email']
            return render_template('signup.html', form=form, email=email)


def is_human(captcha_response):
    """ Validating recaptcha response from google server
        Returns True captcha test passed for submitted form else returns False.
    """
    secret = "6LfgSHMUAAAAAEhiNnOEep3jwRgATmKsdmjEpbl_"
    payload = {'response': captcha_response, 'secret': secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']


@user.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    if session.get('email') is None:
        return render_template('login.html', to_confirm=True)
    else:
        try:
            email = confirm_token(token)
        except:
            return render_template('confirm.html', expired=True)
        con = User.query.filter_by(email=email).first_or_404()
        if con.confirmed:
            return render_template('confirm.html', confirmed=True)
        else:
            con.confirmed = True
            con.confirmed_on = datetime.datetime.now()
            db.session.add(con)
            db.session.commit()
            return render_template('account.html', success=True)


@user.route('/unconfirmed', methods=['GET'])
def unconfirmed():
    if session.get('email') is None:
        return render_template('login.html', )
    else:
        email = session['email']
        con = User.query.filter_by(email=email).first_or_404()
        return render_template('login.html', form=form, email=email)


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = Login(request.form)  # instantiating form to use the forms defined from the Form class in form.py

    if request.method == 'GET':
        if session.get('email') is None:
            return render_template('login.html', form=form)
        else:
            email = session['email']
            return render_template('login.html', form=form, email=email)
    else:
        if not form.validate_on_submit():  # making sure that the form is validated before submission
            return render_template('login.html', form=form)
        else:
            captcha_response = request.form['g-recaptcha-response']
            if is_human(captcha_response):
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
                        return render_template('account.html', login=message)
                    else:
                        if (exists_id is not None) and (exists_email is not None) and (
                                check_password_hash(exists_password, password) is False):
                            return render_template('login.html', invalid=True)
                        else:
                            return render_template('login.html', form=form, not_found=True)
                else:
                    email = session['email']
                    return render_template('login.html', form=form, login=email)
            else:
                # Log invalid attempts
                status = "Sorry ! Bots are not allowed."


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
