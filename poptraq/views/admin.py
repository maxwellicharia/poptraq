import random
from datetime import datetime
from io import BytesIO
from threading import Thread

import pytz
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, login_user
from flask_mail import Message
from flask_weasyprint import render_pdf
from sqlalchemy.exc import InternalError, ProgrammingError
from werkzeug.security import generate_password_hash
from xhtml2pdf import pisa

from poptraq import app, db, mail
from poptraq.decorators import admin_user, anonymous
from poptraq.email import send_email
from poptraq.form import EmailForm, RegistrationForm, SearchForm
from poptraq.models import User
from poptraq.token import generate_confirmation_token, confirm_token

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/', methods=['GET'])
@login_required
@admin_user
def home():
    return render_template('admin/account.html')


@admin.route('/population', methods=['GET'])
@login_required
@admin_user
def population():
    pass


@admin.route('/access_admin', methods=['GET'])
@login_required
@admin_user
def access_admin():
    form = SearchForm()
    results = User.query.filter_by(status='Active').all()
    return render_template('admin/access_admin.html', results=results, form=form)


@admin.route('/search', methods=['GET', 'POST'])
@login_required
@admin_user
def search():
    form = SearchForm()
    if form.validate_on_submit():
        email = request.form['email']
        results = User.query.filter_by(email=email, status='Active').all()
        if not results:
            flash('Admin not Found', category='danger')
            return redirect(url_for('admin.access_admin'))
        flash('Found!', category='success')
        return render_template('admin/access_admin.html', search=results, form=form)
    return redirect(url_for('admin.access_admin'))


@admin.route('/grant_admin_rights/<int:national_id>', methods=['GET'])
@login_required
@admin_user
def grant_admin_rights(national_id):
    user = User.query.get(national_id)
    user.admin = True
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.access_admin'))


@admin.route('/revoke_admin_rights/<int:national_id>', methods=['GET'])
@login_required
@admin_user
def revoke_admin_rights(national_id):
    user = User.query.get(national_id)
    user.admin = False
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.access_admin'))


@admin.route('/grant_user_rights/<int:national_id>', methods=['GET'])
@login_required
@admin_user
def grant_user_rights(national_id):
    user = User.query.get(national_id)
    user.user = True
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.access_admin'))


@admin.route('/revoke_user_rights/<int:national_id>', methods=['GET'])
@login_required
@admin_user
def revoke_user_rights(national_id):
    user = User.query.get(national_id)
    user.user = False
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.access_admin'))


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

        new_user.updated = d_aware.strftime("%B %d, %Y %H:%M:%S")
        new_user.confirmed_on = d_aware.strftime("%B %d, %Y %H:%M:%S")
        new_user.confirmed = True
        new_user.admin = True
        new_user.user = False
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=form.remember_me.data)
        flash("Successful Admin Account Creation", category='success')
        return redirect(url_for('admin.home'))
    return render_template('admin/create_admin.html', form=form, new=True)


@admin.route('/report_dash', methods=['GET'])
@login_required
@admin_user
def report_dash():
    d = datetime.now()
    timezone = pytz.timezone("Africa/Nairobi")
    d_aware = timezone.localize(d)

    date = d_aware.strftime("%B %d, %Y %H:%M:%S")
    results = User.query.filter_by(status='Active').all()
    return render_template('admin/report_dash.html', results=results, date=date)


@admin.route('/reports', methods=['GET'])
@login_required
@admin_user
def reports():
    return render_pdf(url_for('admin.report_pdf'))


@admin.route('/report_pdf', methods=['GET'])
def report_pdf():
    d = datetime.now()
    timezone = pytz.timezone("Africa/Nairobi")
    d_aware = timezone.localize(d)

    date = d_aware.strftime("%B %d, %Y %H:%M:%S")
    results = User.query.filter_by(status='Active').all()
    return render_template('admin/report.html', results=results, date=date)


def create_pdf(pdf_data):
    pdf = BytesIO()
    pisa.CreatePDF(BytesIO(pdf_data.encode('utf-8')), pdf)
    return pdf


@admin.route('/send_report', methods=['GET', 'POST'])
@login_required
@admin_user
def send_report():
    form = EmailForm()
    if form.validate_on_submit():
        subject = "Potraq Report"
        send_report.receiver = form.email.data
        msg = Message(subject, recipients=[send_report.receiver], sender=app.config['MAIL_DEFAULT_SENDER'])
        msg.body = "Find Attached the population analyser (Potraq) Report."
        d = datetime.now()
        timezone = pytz.timezone("Africa/Nairobi")
        d_aware = timezone.localize(d)

        date = d_aware.strftime("%B %d, %Y %H:%M:%S")
        results = User.query.filter_by(status='Active').all()
        pdf = create_pdf(render_template('admin/report.html', results=results, date=date))
        msg.attach("report.pdf", "application/pdf", pdf.getvalue())
        thr = Thread(target=send_async_email, args=[msg])
        thr.start()
        flash('Report sent Successfully to: ' + send_report.receiver, category='success')
        return redirect(url_for('admin.report_dash'))
    return render_template('admin/send_report.html', form=form)


def send_async_email(msg):
    with app.app_context():
        print('====> Sending Email - Async')
        mail.send(msg)


@admin.route('/stats', methods=['GET'])
@login_required
@admin_user
def stats():
    return render_template('admin/stats.html')


def color(i):
    colors = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
              for num in range(i)]
    return colors


@admin.route('/charts', methods=['GET'])
@login_required
@admin_user
def charts():
    fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
    counts = [5, 3, 4, 2, 4, 6]

    source = ColumnDataSource(data=dict(fruits=fruits, counts=counts, color=color(len(fruits))))

    plot = figure(x_range=fruits, y_range=(0, 9), plot_height=500, plot_width=900, title="Fruit Counts",
                  toolbar_location=None, tools="hover")

    plot.vbar(x='fruits', top='counts', width=0.9, color='color', legend="fruits", source=source)

    plot.xgrid.grid_line_color = None
    plot.legend.orientation = "horizontal"
    plot.legend.location = "top_center"

    script, div = components(plot)

    # Return the webpage
    return render_template("admin/charts.html", div=div, script=script)


@admin.route('/analysis', methods=['GET'])
@login_required
@admin_user
def analysis():
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
