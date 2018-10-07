import datetime

from flask import render_template, request, session, Blueprint, url_for, redirect, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse

from poptraq import app, db
from poptraq.email import send_email
from poptraq.form import RegistrationForm, LoginForm, EmailForm, PasswordForm
from poptraq.models import User
from poptraq.user.token import generate_confirmation_token, confirm_token

user = Blueprint('user', __name__, url_prefix='/user', static_folder='static', template_folder='templates')


@user.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('Already logged in as' + current_user.email, category='warning')
        return redirect(url_for('user.account'))
    form = RegistrationForm()
    if form.validate_on_submit():
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
        login_user(new_user, remember=form.remember_me.data)
        send_confirm_link()
        flash('Congratulations, you are now a registered user! Proceed and activate your account', category='success')
        return render_template('unconfirmed.html')
    return render_template('register.html', form=form)


@user.route('/send_link', methods=['GET'])
def send_confirm_link():
    if current_user.is_authenticated:
        new_user = User.query.filter_by(email=current_user.email).first_or_404()
        if new_user.confirmed:
            flash('Account is already activated', category='info')
            return redirect(url_for('user.account'))
        token = generate_confirmation_token(new_user.email)
        confirm_url = url_for('user.confirm_email', token=token, _external=True)
        name = new_user.first_name
        html = render_template('activate.html', confirm_url=confirm_url, name=name)
        subject = "Please confirm your email"
        send_email(new_user.email, subject, html)
        # To thread it and run in the background
        flash('Successfully sent confirmation email', category='success')
        return render_template('unconfirmed.html')
    flash('Login to activate your account', category='danger')
    return redirect(url_for('user.login'))


@user.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('Your confirm link is expired, resending...', category='info')
        send_confirm_link()
        return render_template('confirm.html')
    new_user = User.query.filter_by(email=email).first_or_404()
    if new_user.confirmed:
        flash('Your account is already confirmed', category='info')
        return redirect(url_for('user.account'))
    else:
        new_user.confirmed = True
        new_user.confirmed_on = datetime.datetime.now()
        db.session.add(new_user)
        db.session.commit()
        flash('Successfully confirmed your account', category='success')
        return redirect(url_for('user.account'))


@user.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Already logged in as: ' + current_user.email, category='info')
        return redirect(url_for('index'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        new_user = User.query.filter_by(national_id=form.national_id.data, email=form.email.data).first()
        if new_user is None or not check_password_hash(new_user.password, form.password.data):
            flash('Invalid username or password', category='danger')
            return redirect(url_for('user.login'))
        login_user(new_user, remember=form.remember_me.data)
        if new_user.confirmed:
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('user.account')
            flash('Successful login: ' + current_user.email, category='success')
            return redirect(next_page)
        flash('Confirm your account', category='info')
        return render_template('unconfirmed.html')
    return render_template('login.html', form=form)


@app.route('/recover', methods=["GET", "POST"])
def recover():
    form = EmailForm()
    if request.method == 'GET':
        return render_template('recover.html', form=form)
    else:
        if form.validate_on_submit():
            national_id = form.national_id.data
            email = form.email.data
            exists = db.session.query(User.national_id).filter_by(national_id=national_id, email=email).scalar()
            if (exists.email is not None) and (exists.confirmed is True):
                token = generate_confirmation_token(exists.email)
                confirm_url = url_for('user.reset', token=token, _external=True)
                name = exists.first_name
                html = render_template('reset.html', confirm_url=confirm_url, reset=True, name=name)
                subject = ""
                send_email(exists.email, subject, html)
                # To thread it and run in the background
                return render_template('recover.html', reset=True, email=exists.email)
            else:
                return render_template('unconfirmed.html', link=send_confirm_link())
        else:
            return render_template('recover.html', form=form)


@user.route('/reset/<token>', methods=['GET'])
def reset(token):
    try:
        email = confirm_token(token)
    except:
        flash('Confirm link is expired', category='danger')
        return render_template('confirm.html', expired=True)
    new_user = User.query.filter_by(email=email).first_or_404()
    if new_user.confirmed:
        form = PasswordForm
        return render_template('recover.html', new=True, form=form)
    else:
        return render_template('unconfirmed.html', link=send_confirm_link())


@user.route('/reset/new_password', methods=['GET', 'POST'])
def new_password():
    form = PasswordForm(request.form)
    if request.method == 'GET':
        form = PasswordForm
        return render_template('recover.html', new=True, form=form)
    else:
        if form.validate_on_submit():
            national_id = form.national_id.data
            email = form.email.data
            exists = db.session.query(User.national_id).filter_by(national_id=national_id, email=email).scalar()
            if (exists.email is not None) and (exists.confirmed is True):
                password = generate_password_hash(request.form['password'], method='pbkdf2:sha256',
                                                  salt_length=8)
                exists.password = password
                db.session.add(exists)
                db.session.commit()
                log = LoginForm
                return render_template('login.html', form=log)
            else:
                return render_template('unconfirmed.html', link=send_confirm_link())
        else:
            return render_template('recover.html', new=True, form=form)


@user.route('/logout', methods=['GET'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('Logout successful', category='success')
        return redirect(url_for('index'))
    flash('You are not logged in', category='danger')
    return redirect(url_for('index'))


@user.route('/account', methods=['GET', 'POST'])
def account():
    if current_user.is_authenticated:
        if current_user.confirmed:
            flash('Already logged in as: ' + current_user.email, category='info')
            return render_template('account.html')
        flash('Confirm your account', category='warning')
        return render_template('unconfirmed.html')
    flash('Login to access account', category='warning')
    return render_template('login.html')


app.register_blueprint(user)
