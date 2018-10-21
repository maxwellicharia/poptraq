import pytz
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, login_user
from sqlalchemy.exc import InternalError, ProgrammingError
from werkzeug.security import generate_password_hash

from poptraq import app, db
from poptraq.decorators import admin_user, anonymous
from poptraq.token import generate_confirmation_token, confirm_token
from poptraq.form import EmailForm, RegistrationForm
from poptraq.email import send_email
from poptraq.models import User


admin = Blueprint('admin', __name__, url_prefix='/admin', static_folder='static', template_folder='templates')


@admin.route('/', methods=['GET'])
@login_required
@admin_user
def home():
    return render_template('admin/account.html')


@admin.route('/access_admin', methods=['GET'])
@login_required
@admin_user
def access_admin():
    pass


@admin.route('/add_admin', methods=['GET', 'POST'])
@login_required
@admin_user
def add_admin():
    form = EmailForm()
    if form.validate_on_submit():
        new_admin = User.query.filter_by(email=form.email.data).first()
        if new_admin:
            if new_admin.admin:
                flash('Already and Admin', category='danger')
                return render_template('admin_send_email', form=form)
            flash('User Already Exists but not an Admin, Change Access Rights', category='info')
            return redirect(url_for('user.access_admin'))
        token = generate_confirmation_token(form.email.data)
        confirm_url = url_for('admin.confirm_admin', token=token, _external=True)
        html = render_template('admin/add_admin.html', confirm_url=confirm_url)
        subject = "Admin Account Creation"
        send_email(form.email.data, subject, html)
        flash('Admin Account Creation Link Sent Successfully to: ' + form.email.data, category='success')
        return redirect(url_for('admin.add_admin'))
    return render_template('admin/create_admin.html', form=form, show=True)


@admin.route('/confirm_admin/<token>', methods=['GET'])
@anonymous
def confirm_admin(token):
    try:
        confirm_admin.email = confirm_token(token)
        new_admin = User.query.filter_by(email=confirm_token(token)).first()
        if new_admin:
            if new_admin.admin:
                flash('You Already Have an Account Creation Aborted', category='danger')
                return redirect(url_for('admin.home'))
            flash('Request Access From An Admin', category='info')
            return redirect(url_for('user.account'))
        flash('Fill in Form to Create your Admin Account', category='success')
        form = RegistrationForm()
        return render_template('admin/create_admin.html', form=form, new=True)
    except InternalError and ProgrammingError:
        flash('Your Reset Link is Expired, Try Again', category='danger')
        return redirect(url_for('user.recover'))


@admin.route('/register_admin', methods=['POST'])
@anonymous
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(request.form['national_id'],
                        request.form['first_name'],
                        request.form['surname'],
                        request.form['dob'],
                        request.form['home_county'],
                        request.form['email'],
                        generate_password_hash(request.form['password'], method='pbkdf2:sha256', salt_length=8))
        if confirm_admin.email != form.email.data:
            flash('The Email You have Used was not sent the Admin Account Creation Link, Account Creation Aborted',
                  category='danger')
            return redirect(url_for('index'))
        d = datetime.now()
        timezone = pytz.timezone("Africa/Nairobi")
        d_aware = timezone.localize(d)

        new_user.updated = d_aware.strftime("%B %d, %Y | %H:%M:%S")
        new_user.confirmed_on = d_aware.strftime("%B %d, %Y | %H:%M:%S")
        new_user.confirmed = True
        new_user.admin = True
        new_user.user = False
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=form.remember_me.data)
        flash("Successful Admin Account Creation", category='success')
        return redirect(url_for('admin.home'))
    return render_template('admin/create_admin.html', form=form, new=True)


@admin.route('/reports', methods=['GET'])
@login_required
@admin_user
def reports():
    pass


@admin.route('/statistics', methods=['GET'])
@login_required
@admin_user
def statistics():
    pass


@admin.route('/logs', methods=['GET'])
@login_required
@admin_user
def logs():
    pass


@admin.route('/notifications', methods=['GET'])
@login_required
@admin_user
def notifications():
    pass


@admin.route('/settings', methods=['GET'])
@login_required
@admin_user
def settings():
    pass


@admin.route('/logout', methods=['GET'])
@login_required
@admin_user
def logout():
    logout_user()
    flash('Logout Successful', category='success')
    return redirect(url_for('index'))


app.register_blueprint(admin)
