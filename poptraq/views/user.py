from datetime import datetime

import pytz
from flask import render_template, request, Blueprint, url_for, redirect, flash
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import InternalError, ProgrammingError
from werkzeug.security import generate_password_hash, check_password_hash

from poptraq import app, db
from poptraq.decorators import confirmed, unconfirmed_user, anonymous, normal_user
from poptraq.email import send_email
from poptraq.form import RegistrationForm, EmailForm, PasswordForm, DetailsForm
from poptraq.models import User, Details
from poptraq.token import generate_confirmation_token, confirm_token

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/', methods=['GET'])
@login_required
@normal_user
@unconfirmed_user
def unconfirmed():
    return render_template('user/unconfirmed.html')


@user.route('/account', methods=['GET'])
@login_required
@normal_user
@confirmed
def account():
    return render_template('user/account.html')


@user.route('/register_user', methods=['GET', 'POST'])
@anonymous
def register():
    # Manage accounts using Activity Status
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
    return render_template('app/register.html', form=form)


@user.route('/send_link', methods=['GET'])
@login_required
@normal_user
@unconfirmed_user
def send_confirm_link():
    new_user = User.query.filter_by(email=current_user.email).first_or_404()
    token = generate_confirmation_token(new_user.email)
    confirm_url = url_for('user.confirm_email', token=token, _external=True)
    name = new_user.first_name
    html = render_template('user/activate.html', confirm_url=confirm_url, name=name)
    subject = "Please confirm your email"
    send_email(new_user.email, subject, html)
    flash('Confirmation Email has been sent to: ' + current_user.email, category='success')
    return redirect(url_for('user.unconfirmed'))


@user.route('/confirm/<token>', methods=['GET'])
@login_required
@normal_user
@unconfirmed_user
def confirm_email(token):
    try:
        email = confirm_token(token)
        new_user = User.query.filter_by(email=email).first()
        if new_user.email != current_user.email:
            flash("Link Exists for another Account: " + current_user.email + ". Logout and Login with your account to "
                                                                             "confirm", category='danger')
            return redirect(url_for('user.account'))
        d = datetime.now()
        timezone = pytz.timezone("Africa/Nairobi")
        d_aware = timezone.localize(d)

        new_user.updated = d_aware.strftime("%B %d, %Y %H:%M:%S")
        new_user.confirmed = True
        new_user.confirmed_on = d_aware.strftime("%B %d, %Y %H:%M:%S")
        db.session.add(new_user)
        db.session.commit()
        flash('Successfully Confirmed your Account', category='success')
        return redirect(url_for('user.account'))
    except InternalError and ProgrammingError:
        if current_user.confirmed:
            flash('Your Account is already Confirmed', category='info')
            return redirect(url_for('user.account'))
        flash('Your Confirm Link is Expired, resend to confirm', category='danger')
        return render_template('user/unconfirmed.html')


@user.route('/reset', methods=["GET", "POST"])
def recover():
    if current_user.is_authenticated:
        flash('Already Logged in, Log out to Reset Password', category='warning')
        return redirect(url_for('user.account'))
    form = EmailForm()
    if form.validate_on_submit():
        token = generate_confirmation_token(form.email.data)
        confirm_url = url_for('user.reset', token=token, _external=True)
        html = render_template('user/reset.html', confirm_url=confirm_url)
        subject = "Password Reset"
        send_email(form.email.data, subject, html)
        return render_template('user/recover.html', show=True)
    return render_template('user/recover.html', form=form, reset=True)


@user.route('/reset/<token>', methods=['GET'])
def reset(token):
    if not current_user.is_authenticated:
        try:
            new_user = User.query.filter_by(email=confirm_token(token)).first()
            if new_user:
                flash('Fill in Form to Reset Password', category='success')
                form = PasswordForm()
                return render_template('recover.html', form=form, new=True)
            flash('Invalid Email, Try Again!', category='warning')
            return redirect(url_for('user.recover'))
        except InternalError and ProgrammingError:
            flash('Your Reset Link is Expired, Try Again', category='danger')
            return redirect(url_for('user.recover'))
    flash('You are Logged in, log out to Reset Password', category='warning')
    return redirect(url_for('user.account'))


@user.route('/password_reset', methods=['POST'])
@anonymous
def password_reset():
    form = PasswordForm()
    if form.validate_on_submit():
        new_user = User.query.filter_by(email=reset.email).first()
        if new_user:
            if not check_password_hash(new_user.password, form.password.data):
                d = datetime.now()
                timezone = pytz.timezone("Africa/Nairobi")
                d_aware = timezone.localize(d)

                new_user.updated = d_aware.strftime("%B %d, %Y %H:%M:%S")
                new_user.password = generate_password_hash(form.password.data,
                                                           method='pbkdf2:sha256', salt_length=8)
                db.session.add(new_user)
                db.session.commit()
                flash('Successfully Updated your Password', category='success')
                return redirect(url_for('login'))
            flash('That is your old Password, Reset Aborted', category='info')
            return redirect(url_for('login'))
        flash('Invalid Email, Try Again', category='warning')
        return redirect(url_for('user.recover'))
    return render_template('user/recover.html', form=form, new=True)


@user.route('/details', methods=['GET'])
@login_required
@normal_user
@confirmed
def details():
    form = DetailsForm()
    if form.validate_on_submit():
        detail = Details(request.form['passport_photo'],
                         request.form['age'],
                         request.form['gender'],
                         request.form['marital_status'],
                         request.form['specifics'])
        db.session.add(detail)
        db.session.commit()
        return redirect(url_for('user.account'))
    return render_template('user/details.html', form=form)


@user.route('/notifications', methods=['GET'])
@login_required
@normal_user
@confirmed
def notifications():
    pass


@user.route('/settings', methods=['GET'])
@login_required
@normal_user
@confirmed
def settings():
    pass


@user.route('/logout', methods=['GET'])
@login_required
@normal_user
def logout():
    logout_user()
    flash('Logout Successful', category='success')
    return redirect(url_for('index'))


app.register_blueprint(user)
