import os
from datetime import datetime

import markdown
import pytz
from flask import render_template, send_from_directory, Markup, flash, request, redirect, url_for
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash

from poptraq import app, db
from poptraq.decorators import anonymous
from poptraq.form import LoginForm
from poptraq.models import User


@app.route('/', methods=['GET'])
def index():
    return render_template('app/index.html')


@app.route('/login', methods=['GET', 'POST'])
@anonymous
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(national_id=form.national_id.data, email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data) and user.admin and user.user:
            login_user(user, remember=form.remember_me.data)

            d = datetime.now()
            timezone = pytz.timezone("Africa/Nairobi")
            d_aware = timezone.localize(d)

            user.last_seen = d_aware.strftime("%B %d, %Y | %H:%M:%S")
            db.session.add(user)
            db.session.commit()

            flash('Successful Login SuperAdmin: ' + current_user.email, category='success')
            return redirect(url_for('admin.home'))
        elif user and check_password_hash(user.password, form.password.data) and user.admin:
            login_user(user, remember=form.remember_me.data)

            d = datetime.now()
            timezone = pytz.timezone("Africa/Nairobi")
            d_aware = timezone.localize(d)

            user.last_seen = d_aware.strftime("%B %d, %Y | %H:%M:%S")
            db.session.add(user)
            db.session.commit()

            flash('Successful Login Admin: ' + current_user.email, category='success')
            return redirect(url_for('admin.home'))
        elif user and check_password_hash(user.password, form.password.data) and user.user:
            login_user(user, remember=form.remember_me.data)

            d = datetime.now()
            timezone = pytz.timezone("Africa/Nairobi")
            d_aware = timezone.localize(d)

            user.last_seen = d_aware.strftime("%B %d, %Y | %H:%M:%S")
            db.session.add(user)
            db.session.commit()

            flash('Successful Login User: ' + current_user.email, category='success')
            return redirect(url_for('user.account'))
        flash('Invalid log in credentials, register?', category='danger')
        return redirect(url_for('login'))
    return render_template('app/login.html', form=form)


@app.route('/about', methods=['GET'])
def about():
    with open("./docs/README.md") as f:
        content = f.read()
    content = Markup(markdown.markdown(content))
    return render_template('app/about.html', content=content)


@app.route('/favicon.ico')
def fav():
    return send_from_directory(os.path.join(app.root_path, './static/img'), 'favicon.ico')
