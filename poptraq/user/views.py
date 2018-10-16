import pytz
from datetime import datetime

from flask import render_template, request, Blueprint, url_for, redirect, flash
from flask_login import current_user, login_user, logout_user
from sqlalchemy.exc import InternalError, ProgrammingError
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse

from poptraq import app, db
from poptraq.email import send_email
from poptraq.form import RegistrationForm, LoginForm, EmailForm, PasswordForm
from poptraq.models import User
from poptraq.user.token import generate_confirmation_token, confirm_token

user = Blueprint('user', __name__, url_prefix='/user', static_folder='static', template_folder='templates')


@user.route('/', methods=['GET'])
def unconfirmed():
    if current_user.is_authenticated:
        if current_user.confirmed:
            flash('Account is already confirmed', category='info')
            return redirect(url_for('user.account'))
        return render_template('unconfirmed.html')
    flash('Login to proceed', category='info')
    return redirect(url_for('user.login'))


@user.route('/account', methods=['GET'])
def account():
    if current_user.is_authenticated:
        if current_user.confirmed:
            return render_template('account.html')
        flash('Confirm your account', category='warning')
        return render_template('unconfirmed.html')
    flash('Login to access account', category='warning')
    return redirect(url_for('user.login'))


@user.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('Already logged in as: ' + current_user.email, category='info')
        return redirect(url_for('user.account'))
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(request.form['national_id'],
                        request.form['first_name'],
                        request.form['surname'],
                        request.form['dob'],
                        request.form['home_county'],
                        request.form['email'],
                        generate_password_hash(request.form['password'], method='pbkdf2:sha256', salt_length=8))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=form.remember_me.data)
        send_confirm_link()
        return redirect(url_for('user.unconfirmed'))
    return render_template('register.html', form=form)


@user.route('/send_link', methods=['GET'])
def send_confirm_link():
    if current_user.is_authenticated:
        new_user = User.query.filter_by(email=current_user.email).first_or_404()
        if new_user.confirmed:
            flash('Your account is already confirmed ' + current_user.email, category='info')
            return redirect(url_for('user.account'))
        token = generate_confirmation_token(new_user.email)
        confirm_url = url_for('user.confirm_email', token=token, _external=True)
        name = new_user.first_name
        html = render_template('activate.html', confirm_url=confirm_url, name=name)
        subject = "Please confirm your email"
        send_email(new_user.email, subject, html)
        # To thread it and run in the background
        flash('Account created successfully and sent confirmation email to: ' + current_user.email, category='success')
        return redirect(url_for('index'))
    flash('Login to activate your account', category='danger')
    return redirect(url_for('user.login'))


@user.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    if current_user.is_authenticated:
        try:
            email = confirm_token(token)
            new_user = User.query.filter_by(email=email).first()
            if new_user.confirmed:
                flash('Your account is already confirmed', category='info')
                return redirect(url_for('user.account'))
            d = datetime.now()
            timezone = pytz.timezone("Africa/Nairobi")
            d_aware = timezone.localize(d)

            new_user.updated = d_aware.strftime("%B %d, %Y | %H:%M:%S")
            new_user.confirmed = True
            new_user.confirmed_on = d_aware.strftime("%B %d, %Y | %H:%M:%S")
            db.session.add(new_user)
            db.session.commit()
            flash('Successfully confirmed your account', category='success')
            return redirect(url_for('user.account'))
        except InternalError and ProgrammingError:
            if current_user.confirmed:
                flash('Your account is already confirmed', category='info')
                return redirect(url_for('user.account'))
            flash('Your confirm link is expired', category='danger')
            return render_template('unconfirmed.html')
    flash('You are not logged in', category='warning')
    return redirect(url_for('user.login'))


@user.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Already logged in as: ' + current_user.email, category='info')
        return redirect(url_for('user.account'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        new_user = User.query.filter_by(national_id=form.national_id.data, email=form.email.data).first()
        if new_user is None or not check_password_hash(new_user.password, form.password.data):
            flash('Invalid username or password', category='danger')
            return render_template('login.html', form=form)
        login_user(new_user, remember=form.remember_me.data)

        d = datetime.now()
        timezone = pytz.timezone("Africa/Nairobi")
        d_aware = timezone.localize(d)

        new_user.last_seen = d_aware.strftime("%B %d, %Y | %H:%M:%S")
        db.session.add(new_user)
        db.session.commit()
        if new_user.confirmed:
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('user.account')
            flash('Successful login: ' + current_user.email, category='success')
            return redirect(next_page)
        flash('Confirm your account', category='warning')
        return render_template('unconfirmed.html')
    return render_template('login.html', form=form)


@user.route('/reset', methods=["GET", "POST"])
def recover():
    if current_user.is_authenticated:
        flash('Already logged in, log out to reset password', category='warning')
        return redirect(url_for('user.account'))
    form = EmailForm()
    if form.validate_on_submit():
        token = generate_confirmation_token(form.email.data)
        confirm_url = url_for('user.reset', token=token, _external=True)
        html = render_template('reset.html', confirm_url=confirm_url)
        subject = "Password Reset"
        send_email(form.email.data, subject, html)
        # To thread it and run in the background
        return render_template('recover.html', show=True)
    return render_template('recover.html', form=form, reset=True)


@user.route('/reset/<token>', methods=['GET'])
def reset(token):
    if not current_user.is_authenticated:
        try:
            reset.email = confirm_token(token)
            new_user = User.query.filter_by(email=reset.email).first()
            if new_user:
                flash('Fill in form to reset password', category='success')
                form = PasswordForm()
                return render_template('recover.html', form=form, new=True)
            flash('Invalid email, try again', category='warning')
            return redirect(url_for('user.recover'))
        except InternalError and ProgrammingError:
            flash('Your reset link is expired, try again', category='danger')
            return redirect(url_for('user.recover'))
    flash('You are logged in, log out to proceed', category='warning')
    return redirect(url_for('user.account'))


@user.route('/password_reset', methods=['POST'])
def password_reset():
    form = PasswordForm()
    if form.validate_on_submit():
        new_user = User.query.filter_by(email=reset.email).first()
        if new_user:
            if not check_password_hash(new_user.password, form.password.data):
                d = datetime.now()
                timezone = pytz.timezone("Africa/Nairobi")
                d_aware = timezone.localize(d)

                new_user.updated = d_aware.strftime("%B %d, %Y | %H:%M:%S")
                new_user.password = generate_password_hash(form.password.data,
                                                           method='pbkdf2:sha256', salt_length=8)
                db.session.add(new_user)
                db.session.commit()
                flash('Successfully updated your password', category='success')
                return redirect(url_for('user.login'))
            flash('That is your old password, reset aborted', category='info')
            return redirect(url_for('user.login'))
        flash('Invalid email, try again', category='warning')
        return redirect(url_for('user.recover'))
    return render_template('recover.html', form=form, new=True)


@user.route('/logout', methods=['GET'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('Logout successful', category='success')
        return redirect(url_for('index'))
    flash('You are not logged in', category='danger')
    return redirect(url_for('index'))


app.register_blueprint(user)
